from database import server

class ClientID():

    def __init__(self):
        pass

    def min(self):
        query = "SELECT MIN(clientID) FROM contabyx.Clients"
        cursor = server.New().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]

    def max(self):
        query = "SELECT MAX(clientID) FROM contabyx.Clients"
        cursor = server.New().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]