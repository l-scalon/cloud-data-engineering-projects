import mysql.connector as mysql
from database.variables import Variable as env

class MySQL:

    def __init__(self) -> None:
        pass

    def connect(self, database: str = None, autocommit = True):
        connection = mysql.connect(host = env().get('HOST'), 
                                    user = env().get('SQLUSER'), 
                                    passwd = env().get('PASSWORD'), 
                                    database = database, 
                                    autocommit = autocommit)
        connection.set_charset_collation(charset = 'utf8mb4', collation = 'utf8mb4_0900_ai_ci')
        return connection