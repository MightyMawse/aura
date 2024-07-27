import asyncio
import sqlite3
from enum import Enum
import MySQLdb

class Globals:
    loggedInUsers = {} # ID, class
    AWSEndpoint = "aura-database.choigo0y258e.ap-southeast-2.rds.amazonaws.com"

    # Query sql server
    @staticmethod
    def SQL_query(query):
        con = MySQLdb.connect(host=Globals.AWSEndpoint,
                     user="admin", 
                     passwd="negativeG",
                     db="aura-database")
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        return cur.fetchall()

    # Get sql values and convert to class instance
    @staticmethod
    def SQL_to_obj(self, query, type):
        sqlQuery = self.SQL_query(query)
        for row in sqlQuery:
            try:
                pass # Try convert sql row into obj of type
            except:
                continue
        return None