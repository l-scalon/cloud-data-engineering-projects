from random import randint, uniform
from database import server, select
from generate import client

class Client():
    
    def __init__(self):
        pass

    def new(self, type:str):
        name, document, number = client.New(type).fake()
        query = "EXECUTE contabyx.contabyx.new_client_{} '{}', '{}', {}".format(type, name, document.upper(), number)
        server.New().cursor.execute(query).commit()

class Transaction():

    def __init__(self):
        self.min = select.ClientID().min()
        self.max = select.ClientID().max()

    def new(self, type:str):
        try:
            clientID, amount = randint(self.min, self.max), round(uniform(1000, 50000), 2)
            query = "EXECUTE contabyx.new_transaction_{} {}, {}".format(type, clientID, amount)
            server.New().cursor.execute(query).commit()
        except: pass

class Transfer():

    def __init__(self):
        self.min = select.ClientID().min()
        self.max = select.ClientID().max()
    
    def new(self):
        try:
            clientID_origin, clientID_target, amount = randint(self.min, self.max), randint(self.min, self.max), round(uniform(1000, 50000), 2)
            query = "EXECUTE contabyx.new_transfer {}, {}, {}".format(clientID_origin, clientID_target, amount)
            server.New().cursor.execute(query).commit()
        except: pass