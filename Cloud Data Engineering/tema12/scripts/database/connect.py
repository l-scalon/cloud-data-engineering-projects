import mysql.connector as server
import pyodbc as redshift
from database.variables import Variable as env

class MySQL:

    def __init__(self) -> None:
        pass

    def connect(self, database: str = None, autocommit = True):
        connection = server.connect(host = env().get('HOST'), 
                                    user = env().get('USER'), 
                                    passwd = env().get('PASSWORD'), 
                                    database = database, 
                                    autocommit = autocommit)
        connection.set_charset_collation(charset = 'utf8mb4', collation = 'utf8mb4_0900_ai_ci')
        return connection

class Redshift:

    def __init__(self) -> None:
        pass

    def connect(self):
        connection = redshift.connect('DSN=Redshift')
        return connection