import mysql.connector as server

def connect(database:str = None):
    return server.connect(host = 'localhost', user = 'root', passwd = '<PASSWORD>', database = database, autocommit = True)