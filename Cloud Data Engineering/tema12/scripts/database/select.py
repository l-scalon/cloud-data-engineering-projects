from database.connect import MySQL
from database.execute import Query

class Table:

    def __init__(self) -> None:
        self.connection = MySQL().connect('contabyx')

    def select(self, table: str):
        query = f"SELECT * FROM {table}"
        return Query().execute(self.connection, query)

class Client:

    def __init__(self) -> None:
        self.connection = MySQL().connect('contabyx')

    def min(self) -> int:
        query = "SELECT MIN(clientID) FROM Clients"
        return Query().execute(self.connection, query)[0][0]

    def max(self) -> int:
        query = "SELECT MAX(clientID) FROM Clients"
        return Query().execute(self.connection, query)[0][0]

class Document:

    def __init__(self) -> None:
        self.connection = MySQL().connect('contabyx')

    def typeID(self, document: str):
        query = f"SELECT documentTypeID FROM DocumentTypes WHERE initials = '{document}'"
        typeID = Query().execute(self.connection, query)
        if len(typeID) == 0: return None
        else: return typeID[0][0]

class Transaction:

    def __init__(self) -> None:
        self.connection = MySQL().connect('contabyx')

    def typeID(self, nature: str, type: str):
        query = f"SELECT typeID FROM TransactionTypes WHERE nature = '{nature}' AND transactionType = '{type}'"
        typeID = Query().execute(self.connection, query)
        if len(typeID) == 0: return None
        else: return typeID[0][0]

    def max(self) -> int:
        query = "SELECT MAX(transactionID) FROM Transactions"
        return Query().execute(self.connection, query)[0][0]

    def taxID(self, transaction_type: int) -> int:
        query = f"SELECT taxTypeID FROM TaxType WHERE typeID = '{transaction_type}'"
        return Query().execute(self.connection, query)[0][0]

    def rate(self, taxID: int) -> float:
        query = f"SELECT rate FROM TaxType WHERE typeID = '{taxID}'"
        return Query().execute(self.connection, query)[0][0]

    def max_transfer(self) -> int:
        query = "SELECT MAX(transferID) FROM Transfers"
        return Query().execute(self.connection, query)[0][0]