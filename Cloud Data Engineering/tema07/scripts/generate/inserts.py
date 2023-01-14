from random import randint, uniform
from generate import natural, legal
from database.insert import Insert
from database.select import ClientID

class Client():

    def __init__(self):
        self.parameter = 'clients'

    def natural(self):
        info = natural.get()
        insert = "CALL new_client_natural ('{}', '{}', {});".format(info[0], info[1].upper(), info[2])
        Insert().statement(insert)

    def legal(self):
        info = legal.get()
        insert = "CALL new_client_legal ('{}', '{}', {});".format(info[0], info[1].upper(), info[2])
        Insert().statement(insert)

    def new(self, natural:int, legal:int):
        while natural or legal > 0:
            for _ in range(randint(0, 10)):
                if natural > 0 and randint(0, 10) <= 5:
                    self.natural()
                    natural -= 1
            if legal > 0 and randint(0, 10) <= 5:
                self.legal()
                legal -= 1

class Transaction():

    def __init__(self):
        self.parameter = 'transactions'

    def expense(self):
        insert = "CALL new_transaction_expense ({}, {});".format(randint(ClientID().get_min(), ClientID().get_max()), round(uniform(1000, 50000), 2))
        Insert().statement(insert)

    def income(self):
        insert = "CALL new_transaction_income({}, {});".format(randint(ClientID().get_min(), ClientID().get_max()), round(uniform(1000, 50000), 2))
        Insert().statement(insert)

    def transfer(self):
        insert = "CALL new_transfer({}, {}, {});".format(randint(ClientID().get_min(), ClientID().get_max()), randint(ClientID().get_min(), ClientID().get_max()), round(uniform(1000, 50000), 2))
        Insert().statement(insert)

    def new(self, expense:int, income:int, transfer:int):
        while expense or income or transfer > 0:
            for _ in range(randint(0, 5)):
                if transfer > 0:
                    self.transfer()
                    transfer -= 1
            if expense > 0 and randint(0, 10) <= 5:
                self.expense()
                expense -= 1
            if income > 0 and randint(0, 10) <= 5:
                self.income()
                income -= 1