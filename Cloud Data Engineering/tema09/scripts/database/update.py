from database.server import SQLServer as sql
from generate.datetime import Datetime as dt
from database.select import Transfers
from database.insert import TransactionTypes

class Update():

    def __init__(self):
        pass

    def update(self, table: str, column: str, update_parameter: str, id_column: str, id_parameter: int):
        query = '''
                    UPDATE {}
                    SET {} = {}
                    WHERE {} = {}'''.format(table, column, update_parameter, id_column, id_parameter)
        sql().cursor.execute(query).commit()
        
class Datetime(Update):

    def __init__(self):
        pass

    def random(self, transactionsID = []):
        datetime = dt().random()
        table = 'contabyx.Transactions'
        column = 'time'
        update_parameter = "CAST('{}' AS DATETIME)".format(datetime)
        id_column = 'transactionID'
        for id_parameter in transactionsID:
            if not id_parameter == None: self.update(table, column, update_parameter, id_column, id_parameter)

    def all(self):
        transfers = Transfers().transaction_ID()
        difference = TransactionTypes().get_difference()
        for transactiondsID in transfers: self.random(transactiondsID)
        for i in difference: self.random([i])