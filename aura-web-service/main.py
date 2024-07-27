from flask import Flask
from flask import request
import user
import globals

app = Flask(__name__)

@app.route("/register")
def register(): # Takes query param (username, password)
    username = request.args.get("username")
    password = request.args.get("password")

    # Store username, password, userID to SQL Web service
    # Check if exists
    checkQuery = 'SELECT COUNT(*) FROM users WHERE username = "{0}" AND password = "{1}";'.format(username, password)
    queryResult = globals.Globals.SQL_query(checkQuery)
    if(queryResult[0][0] > 0):
        return "Account Already Exists"
    else:
        addQuery = 'INSERT INTO users (username, password, groupID) VALUES("{0}", {1}, 5);'.format(username, password)
        globals.Globals.SQL_query(addQuery)
        return "Account Created Successfully", 200

@app.route("/alter-group")
def alter_group(): # Takes query param (action=CREATE/DELETE, group_name, group_ID(optional))
    action = request.args.get("action")
    groupName = request.args.get("group_name")
    groupID = request.args.get("group_ID")

    query = ""
    if(action == "CREATE"):
        query = "INSERT INTO partys (groupName) VALUES({0})".format(groupName)

    elif(action == "DELETE"):
        query = "DELETE FROM partys WHERE groupID = {0};".format(groupID)
    
    globals.Globals.SQL_query(query)

@app.route("/login")
def login(): # Takes query param (username, password)
    # Fetch user data from db
    # Add to logged in users
    username = request.args.get("username")
    password = request.args.get("password")

    userQuery = 'SELECT * FROM users WHERE username = "{0}" AND password = "{1}";'.format(username, password)
    response = globals.Globals.SQL_query(userQuery)
    
    loggedInUser = user.User(response[0][2])
    loggedInUser.aura = response[0][3]
    loggedInUser.userID = response[0][0]

    # Add to currently logged in users
    globals.Globals.loggedInUsers.update({loggedInUser.userID: loggedInUser})
    return "Login Successful"

@app.route("/vote")
def vote(): # Takes query param (userID, groupID, targetID, value)
    pass

@app.route("/manip-user")
def manip_user(): # Takes query param (userID, variable_name, value) # special values: variable_name=JOIN/LEAVE
    userID = request.args.get("userID")
    variableName = request.args.get("variable_name")
    value = request.args.get("value")

    if(variableName == "JOIN"):
        # Check if already in group
        # Add to group
        pass
    elif(variableName == "LEAVE"):
        pass
    else:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
