from database import server
from database.query import Query

class ClientID:

    def __init__(self):
        self.database_connection = server.connect('contabyx')

    def get_min(self):
        query = 'SELECT MIN(clientID) FROM Clients'
        result = Query().statement(query, self.database_connection)
        return result[0][0]

    def get_max(self):
        query = 'SELECT MAX(clientID) FROM Clients'
        result = Query().statement(query, self.database_connection)
        return result[0][0]