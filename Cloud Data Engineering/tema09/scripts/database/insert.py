from random import randint, uniform, choice
from database import select
from database.server import SQLServer as sql
from generate import client
from generate.datetime import Datetime as dt

class Insert():

    def insert(self, query):
        sql().cursor.execute(query).commit()

    def get_type(self, client = 'natural', nature = 'income'):
        income = ['wages', 'deposit', 'allowance', 'interest', 'benefits', 'sales', 'operating', 'exceptional', 'services', 'royalties']
        expense = ['personal', 'bills', 'deposit', 'application', 'leasing', 'wages', 'bills', 'exceptional', 'contract', 'purchases']

        match client, nature:
            case 'natural', 'income':
                return choice(income[0:4])
            case 'natural', 'expense':
                return choice(expense[0:4])
            case 'legal', 'income':
                return choice(income[5:9])
            case 'legal', 'expense':
                return choice(expense[5:9])

class Client(Insert):
    
    def __init__(self):
        pass

    def new(self, type:str):
        name, document, number = client.New(type).fake()
        query = "EXECUTE contabyx.contabyx.new_client_{} '{}', '{}', {}".format(type, name, document.upper(), number)
        self.insert(query)

class Transaction(Insert):

    def __init__(self):
        self.min = select.ClientID().min()
        self.max = select.ClientID().max()

    def new(self, nature:str):
        try:
            clientID, amount = randint(self.min, self.max), round(uniform(1000, 50000), 2)
            client = select.Clients().type(clientID)
            type = self.get_type(client, nature)
            datetime = dt().random()
            query = "EXECUTE contabyx.new_transaction_{} {}, {}, '{}', '{}'".format(nature, clientID, amount, type, datetime)
            self.insert(query)
        except: pass

class Transfer(Insert):

    def __init__(self):
        self.min = select.ClientID().min()
        self.max = select.ClientID().max()
    
    def new(self):
        try:
            clientID_origin, clientID_target, amount = randint(self.min, self.max), randint(self.min, self.max), round(uniform(1000, 50000), 2)
            datetime = dt().random()
            query = "EXECUTE contabyx.new_transfer {}, {}, {}, '{}'".format(clientID_origin, clientID_target, amount, datetime)
            self.insert(query)
        except: pass

class TransactionTypes(Insert):

    def __init__(self):
        self.transfers = select.Transfers().transaction_ID()

    def transactionsID_on_Transfers(self):
        transactionsID_on_Transfers = []
        for row in self.transfers:
            for transactionID in row:
                if not transactionID == None:
                    transactionsID_on_Transfers.append(transactionID)
        return transactionsID_on_Transfers

    def insert_transfers(self):
        for row in self.transfers:
            type = self.get_type()
            for transactionID in row:
                if not transactionID == None:
                    query = "INSERT contabyx.TransactionTypes(transactionID, transaction_type) VALUES ({}, '{}')".format(transactionID, type)
                    self.insert(query)

    def get_difference(self):
        transactions = select.Transactions().transaction_ID()
        transactionsID = []
        for row in transactions:
            transactionsID.append(row[0])
        difference = set(transactionsID).difference(self.transactionsID_on_Transfers())
        return difference


    def insert_randoms(self):
        difference = self.get_difference()
        for transactionID in difference:
            nature = select.Transactions().nature(transactionID)
            clientID = select.Transactions().clientID(transactionID)
            client = select.Clients().type(clientID)
            type = self.get_type(client, nature)
            query = "INSERT contabyx.TransactionTypes(transactionID, transaction_type) VALUES ({}, '{}')".format(transactionID, type)
            self.insert(query)