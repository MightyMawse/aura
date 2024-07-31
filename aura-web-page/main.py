from flask import *
import json
import os

app = Flask(__name__)

@app.route("/")
def root():
   return render_template("login.html")

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, port=5000)