import json
import os
import sql_interface
import vote
from flask import *
from flask import Request

app = Flask(__name__)

# Terrible design, refactor later
voteMap = {"6": []}

def init():
   # Initialise voteMap
   query = "SELECT * FROM party;"
   groups = sql_interface.SQLInterface.SQL_query(query)
   for group in groups:
      voteMap.update({group[0], []})

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
   return "Ok"

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
   voteMap[str(groupID)].append(newVote) # Add vote to vote map
   return "Ok"

# Return list of all votes that are active on groupID
@app.route("/check_votemap", methods=["GET"])
def check_votemap():
   groupID = request.args.get("groupID")
   jsonVote = []
   if(len(voteMap[groupID]) > 0):
      for vote in voteMap[groupID]:
         jsonVote.append(json.dumps(vote.__dict__))
   return jsonVote

# Get user via userID
@app.route("/get_user", methods=["GET"])
def get_user():
   userID = request.args.get("userID")
   query = sql_interface.SQLInterface.queryMap["GET_USER"].format(userID)
   user = sql_interface.SQLInterface.SQL_query(query)
   return json.dumps(user)

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, port=5000)
   init()