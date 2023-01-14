from database.connect import MySQL
from database.execute import Query

class Client:

    def __init__(self) -> None:
        self.connection = MySQL().connect('contabyx')

    def min(self) -> int:
        query = "SELECT MIN(clientID) FROM Clients"
        return Query().execute(self.connection, query)[0][0]

    def max(self) -> int:
        query = "SELECT MAX(clientID) FROM Clients"
        return Query().execute(self.connection, query)[0][0]