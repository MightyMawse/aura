import json
import os
import sql_interface
from flask import *
from flask import Request

app = Flask(__name__)

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

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, port=5000)