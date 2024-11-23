import json
import os
import sql_interface
import vote
import aura
from flask import *
from flask import Request

app = Flask(__name__)

@app.route("/")
def root():
   aura.Init()
   return render_template("login.html")

# Get page
@app.route("/page")
def page():
   page = request.args.get("name")
   return render_template(page + ".html")

# Raw SQL query, potential vulnerability
@app.route("/sql_query", methods=['POST'])
async def sql_query():
   jsonObj = request.json
   query = jsonObj["query"]
   out = sql_interface.SQLInterface.SQL_query(query)
   return json.dumps(out)

# Check if account exists, returning COUNT(*)
@app.route("/check_account", methods=['GET'])
async def check_account():
   username = request.args.get("username")
   password = request.args.get("password")
   out = sql_interface.SQLInterface.GetAccount(username, password)
   return json.dumps(out)

# Create account, do internal check if exists, dont trust client side one
@app.route("/create_account", methods=["POST"])
async def create_account():
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
async def get_aura():
   userID = request.args.get("userID")
   out = sql_interface.SQLInterface.GetAura(userID)
   return json.dumps(out)

# Get group members by groupID
@app.route("/get_groupmembers", methods=["GET"])
async def get_groupmembers():
   groupID = request.args.get("groupID")
   out = sql_interface.SQLInterface.GetMembers(groupID)
   return json.dumps(out)

# Get members in group that arent me
@app.route("/get_groupmembers_exclusive", methods=["GET"])
async def get_groupmembers_exclusive():
   groupID = request.args.get("groupID")
   userID = request.args.get("userID")
   return await aura.GetGroupMembersExclusive(groupID, userID)

@app.route("/callvote", methods=["POST"])
async def callvote():
   # Create new vote class instance and add to votemap, 
   # vote instance will stay until resolved by group members
   jsonObj  = request.json # POST body
   groupID  = jsonObj["groupID"]
   auraVal  = jsonObj["aura"]
   targetID = jsonObj["targetID"]
   senderID = jsonObj["senderID"]

   return await aura.CallVote(groupID, auraVal, targetID, senderID)

# Return list of all votes that are active on groupID
@app.route("/check_votemap", methods=["GET"])
async def check_votemap():
   groupID = request.args.get("groupID")
   userID = request.args.get("userID")
   return await aura.CheckVoteMap(groupID, userID)

# Submit vote to votemap
@app.route("/submit_vote", methods=["POST"])
async def submit_vote():
   jsonObj = request.json
   userID  = jsonObj["userID"]
   groupID = jsonObj["groupID"]
   vote    = jsonObj["vote"]
   return await aura.SubmitVote(userID, groupID, vote)

# Get user via userID
@app.route("/get_user", methods=["GET"])
async def get_user():
   userID = request.args.get("userID")
   query = sql_interface.SQLInterface.queryMap["GET_USER"].format(userID)
   user = sql_interface.SQLInterface.SQL_query(query)
   return json.dumps(user)

# Check for required updates on our group
@app.route("/check_update", methods=["GET"])
async def check_update():
   groupID = request.args.get("groupID")
   userID = request.args.get("userID")
   return await aura.CheckUpdate(groupID, userID)

@app.route("/group_code", methods=["GET"])
async def group_code():
   groupID = request.args.get("groupID")
   return await aura.GroupCode(groupID)

@app.route("/get_group", methods=["GET"])
async def get_group():
   groupID = request.args.get("groupID")
   return await sql_interface.SQLInterface.GetGroup(groupID)

# This is a HACK fix later if modularizing group system
@app.route("/join", methods=["GET"])
async def join():
   groupCode = request.args.get("groupCode")
   userID = request.args.get("userID")
   return await aura.Join(groupCode, userID)

if __name__ == '__main__':
   #init()
   app.run(host='0.0.0.0', debug=True, port=5000)