import MySQLdb

class SQLInterface:
    AWSEndpoint = "aura-database.choigo0y258e.ap-southeast-2.rds.amazonaws.com"

    queryMap = {
        "GET_ACCOUNT": 'SELECT COUNT(*) FROM users WHERE username = "{0}" AND password = "{1}";',
        "CREATE_ACCOUNT": 'INSERT INTO users (username, aura, password) VALUES("{0}", "{1}", "{2}");'
    }

    # Query sql server
    @staticmethod
    def SQL_query(query):
        con = MySQLdb.connect(host=SQLInterface.AWSEndpoint,
                     user="admin", 
                     passwd="negativeG",
                     db="aura-database")
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        return cur.fetchall()
    
    # Get account with details count
    @staticmethod
    def GetAccount(username, password):
        query = SQLInterface.queryMap["GET_ACCOUNT"].format(username, password)
        out = SQLInterface.SQL_query(query)
        return out
