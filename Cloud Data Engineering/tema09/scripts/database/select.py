from database.server import SQLServer as sql

class ClientID():

    def __init__(self):
        pass

    def min(self):
        query = "SELECT MIN(clientID) FROM contabyx.Clients"
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]

    def max(self):
        query = "SELECT MAX(clientID) FROM contabyx.Clients"
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]

class Transfers():

    def __init__(self):
        pass

    def transaction_ID(self):
        query = "SELECT expense_transactionID, income_transactionID FROM contabyx.Transfers"
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchall()

    def expense_transactionID(self):
        query = "SELECT expense_transactionID FROM contabyx.Transfers"
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchall()

class TransactionID():

    def __init__(self):
        pass

    def transaction_ID(self, table: str):
        query = "SELECT transactionID FROM contabyx.{}".format(table)
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchall()

    def min(self):
        query = "SELECT MIN(transactionID) FROM contabyx.Transactions"
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]

    def max(self):
        query = "SELECT MAX(transactionID) FROM contabyx.Transactions"
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]

class Transactions():

    def __init__(self):
        pass

    def transaction_ID(self):
        return TransactionID().transaction_ID('Transactions')

    def nature(self, transactionID: int):
        query = "SELECT nature FROM contabyx.Transactions WHERE transactionID = {}".format(transactionID)
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]

    def clientID(self, transactionID: int):
        query = "SELECT clientID FROM contabyx.Transactions WHERE transactionID = {}".format(transactionID)
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]

class TransactionTypes():

    def _init_(self):
        pass

    def transaction_ID(self):
        return TransactionID().transaction_ID('TransactionTypes')

class Clients():

    def __init__(self):
        pass

    def type(self, clientID):
        query = "SELECT type FROM contabyx.Clients WHERE clientID = {}".format(clientID)
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]