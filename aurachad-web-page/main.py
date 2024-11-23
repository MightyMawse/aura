import json
import os
import sql_interface
import vote
import aura
from flask import *
from flask import Request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
clients = []

@app.route("/")
def root():
   aura.Init()
   return render_template("login.html")

@socketio.on("refresh")
def handle_refresh(room):
   print(str(request.sid) + " requests a dashboard refresh")
   socket_broadcast("refresh", "FLAG", room)

@socketio.on("call_vote")
def handle_vote(data):
   jsonData = json.loads(data)
   callvote(jsonData)
   socket_broadcast(jsonData, "VOTECALL", jsonData["room"])

@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    socket_direct(request.sid, "Hello " + str(request.sid), "MSG")

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    clients.append(request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

# Get page
@app.route("/page")
def page():
   page = request.args.get("name")
   return render_template(page + ".html")

# Broadcasts to all clients connected via socket
def socket_broadcast(msg, type, room):
   msgObj = {"type" : type, "content": msg}
   send(json.dumps(msgObj), to=room)

def socket_direct(sid, msg, type):
   msgObj = {"type" : type, "content": msg}
   send(msgObj, to=sid)

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

# Called by socket
def callvote(json):
   # Create new vote class instance and add to votemap, 
   # vote instance will stay until resolved by group members
   jsonObj  = json # POST body
   groupID  = jsonObj["groupID"]
   auraVal  = jsonObj["aura"]
   targetID = jsonObj["targetID"]
   senderID = jsonObj["senderID"]

   return aura.CallVote(groupID, auraVal, targetID, senderID)

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
   #socketio.run(app, debug=True)