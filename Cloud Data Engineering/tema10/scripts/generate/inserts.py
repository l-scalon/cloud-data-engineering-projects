from pydoc import cli
from bson import ObjectId
from database.connect import MongoDB
from database.document import Client, Transaction
from database.insert import New_Client, New_Transaction, New_Transfer
from database.select import Collection
from generate.fake import Client as fake_client
from random import choice, randint, uniform

class Random():

    def __init__(self):
        pass

    def client(self, type: str):
        fake = fake_client().fake(type)
        new_client = Client(type = type, name = fake[0], documents = {fake[1].upper(): fake[2]})
        New_Client().insert(new_client)

    def type(self, client = 'natural', nature = 'income'):
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

    def datetime(self)->str:
        years = [2019, 2020, 2021, 2022]
        seed = randint(1, 41)
        floor = seed // 12
        year = years[floor]
        month = (seed % 12) + 1
        if month == 2: day = randint(1, 28)
        else: day = randint(1, 30)
        hour, minutes, seconds = randint(0, 23), randint(0, 59), randint(0, 59)

        return '{}-{}-{} {}:{}:{}.000'.format(year, month, day, hour, minutes, seconds)

    def transaction(self, nature = None, transfer = False):
        database = MongoDB().get_database('contabyx')
        collection = database['Clients']
        fetch_IDs = Collection().select(collection = collection, columns = ["_id"])
        client_IDs = []

        for id in fetch_IDs:
            client_ID = id.get("_id")
            client_IDs.append(client_ID)

        clients = ['natural', 'legal']
        client = choice(clients)
        type = self.type(client, nature)
        time = self.datetime()
        amount = round(uniform(1000, 50000), 2)

        if transfer == False:
            new_transaction = Transaction(clientID = choice(client_IDs), nature = nature, type = type, time = time, amount = amount)
            New_Transaction().insert(new_transaction)

        else:
            New_Transfer().insert(from_clientID = choice(client_IDs), to_clientID = choice(client_IDs), type = type, time = time, amount = amount)

class Batch():

    def __init__(self):
        pass

    def insert(self, clients: list, transactions: int):
        for _ in range(clients[0]):
            Random().client('natural')
        for _ in range(clients[1]):
            Random().client('legal')
        for _ in range(transactions):
            Random().transaction('income')
            Random().transaction('expense')
            Random().transaction(transfer = True)