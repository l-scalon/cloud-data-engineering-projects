from database import server
from math import isclose

class Compare():

    def __init__(self, old, new, tables:list):
        self.old = old
        self.new = new
        self.tables = tables

    def is_equal(self, query = '*'):
        for table in self.tables:
            select = 'SELECT {} FROM contabyx.{}'.format(query, table)
            self.old.cursor.execute(select)
            self.new.cursor.execute(select)
            for result_old, result_new in zip(self.old.cursor.fetchall(), self.new.cursor.fetchall()):
                if all(old == new for old, new in zip(result_old, result_new)): equals = True
                else: equals = False
            print('{}: {}'.format(table, equals))

    def is_close(self, query = '*'):
        for table in self.tables:
                select = 'SELECT {} FROM contabyx.{}'.format(query, table)
                self.old.cursor.execute(select)
                self.new.cursor.execute(select)
                for result_old, result_new in zip(self.old.cursor.fetchall(), self.new.cursor.fetchall()):
                    if all(isclose(float(old), float(new), abs_tol = 0.1) for old, new in zip(result_old, result_new)): equals = True
                    else: equals = False
                print('{}: {}'.format(table, equals))

def main():
    Compare(server.Old(), server.New(), ['Clients', 'Documents', 'Transfers']).is_equal()
    Compare(server.Old(), server.New(), ['Transactions']).is_equal('transactionID, clientID, nature')
    Compare(server.Old(), server.New(), ['Tax']).is_equal('transactionID')
    Compare(server.Old(), server.New(), ['Transactions']).is_close('ROUND(amount, 2)')
    Compare(server.Old(), server.New(), ['Tax']).is_close('ROUND(rate, 2), ROUND(fee, 2)')