import json
import os
import sql_interface
import vote
from flask import *
from flask import Request

app = Flask(__name__)

# Terrible design, refactor later, should be compressed into group class
voteMap = {}
updateFlag = [] # groupIDs that need data updated

def init():
   # Initialise voteMap
   query = "SELECT * FROM party;"
   groups = sql_interface.SQLInterface.SQL_query(query)
   for group in groups:
      voteMap.update({str(group[0]): None})

@app.route("/")
def root():
   return render_template("login.html")

# Get page
@app.route("/page")
def page():
   page = request.args.get("name")
   return render_template(page + ".html")

# Raw SQL query, potential vulnerability
@app.route("/sql_query", methods=['POST'])
def sql_query():
   jsonObj = request.json
   query = jsonObj["query"]
   out = sql_interface.SQLInterface.SQL_query(query)
   return json.dumps(out)

# Check if account exists, returning COUNT(*)
@app.route("/check_account", methods=['GET'])
def check_account():
   username = request.args.get("username")
   password = request.args.get("password")
   out = sql_interface.SQLInterface.GetAccount(username, password)
   return json.dumps(out)

# Create account, do internal check if exists, dont trust client side one
@app.route("/create_account", methods=["POST"])
def create_account():
   jsonObj = request.json
   username = jsonObj["username"]
   password = jsonObj["password"]

   # Check if exists
   query = sql_interface.SQLInterface.queryMap["CREATE_ACCOUNT"].format(username, 100, password)
   count = sql_interface.SQLInterface.GetAccount(username, password)
   if(count[0][0] == 0):
      sql_interface.SQLInterface.SQL_query(query) # Create account
   return json.dumps("Ok")

# Get user aura count by userID
@app.route("/get_aura", methods=["GET"])
def get_aura():
   userID = request.args.get("userID")
   out = sql_interface.SQLInterface.GetAura(userID)
   return json.dumps(out)

# Get group members by groupID
@app.route("/get_groupmembers", methods=["GET"])
def get_groupmembers():
   groupID = request.args.get("groupID")
   out = sql_interface.SQLInterface.GetMembers(groupID)
   return json.dumps(out)

@app.route("/callvote", methods=["POST"])
def callvote():
   # Create new vote class instance and add to votemap, 
   # vote instance will stay until resolved by group members
   jsonObj  = request.json # POST body
   groupID  = jsonObj["groupID"]
   aura     = jsonObj["aura"]
   targetID = jsonObj["targetID"]
   senderID = jsonObj["senderID"]

   newVote = vote.Vote(groupID, aura, targetID, senderID)
   voteMap[str(groupID)] = newVote # Change vote, subsequent votes with overwrite if not resolved
   return json.dumps("Ok")

# Return list of all votes that are active on groupID
@app.route("/check_votemap", methods=["GET"])
def check_votemap():
   groupID = request.args.get("groupID")
   userID = request.args.get("userID")
   if(voteMap[groupID] != None):
      if(int(userID) in voteMap[groupID].groupMemberIDs):
         return json.dumps(voteMap[groupID].__dict__) # Only send if vote is waiting on sender userID
   return json.dumps("Ok")

# Submit vote to votemap
@app.route("/submit_vote", methods=["POST"])
def submit_vote():
   jsonObj = request.json
   userID = jsonObj["userID"]
   groupID = jsonObj["groupID"]

   vc = voteMap[str(groupID)]
   if(int(userID) in vc.groupMemberIDs):
      voteMap[str(groupID)].groupMemberIDs.remove(int(userID))
   return json.dumps("Ok")

# Get user via userID
@app.route("/get_user", methods=["GET"])
def get_user():
   userID = request.args.get("userID")
   query = sql_interface.SQLInterface.queryMap["GET_USER"].format(userID)
   user = sql_interface.SQLInterface.SQL_query(query)
   return json.dumps(user)

# Check for required updates on our group
@app.route("/check_update", methods=["GET"])
def check_update():
   groupID = request.args.get("groupID")

   if(voteMap[str(groupID)] != None):
      voteMap[str(groupID)].CheckVote()

   if(groupID in updateFlag):
      return json.dumps("UPDATE")
   return json.dumps("Ok")

if __name__ == '__main__':
   init()
   app.run(host='0.0.0.0', debug=True, port=5000)