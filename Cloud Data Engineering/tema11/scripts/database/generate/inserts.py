from random import randint, choice, uniform
from faker import Faker
from database.connect import MySQL
from database.select import Client as id
from database.execute import Query

class Random:

    def __init__(self) -> None:
        pass

    def client(self, nature: str) -> dict:
        fake = Faker(locale = 'pt_BR')
        match nature:
            case 'natural': return {'name': fake.name(), 'document': fake.lexify(text = '???'), 'number': fake.numerify(text = '##########')}
            case 'legal': return {'name': fake.company(), 'document': fake.lexify(text = '????'), 'number': fake.numerify(text = '##########0001')}

    def transaction(self, transaction = None) -> dict:
        if not transaction == None:
            transaction['clientID_to'] = randint(id().min(), id().max())
            return transaction

        clientID = randint(id().min(), id().max())
        time = self.time()
        amount = round(uniform(500, 50000))
        nature = choice(['income', 'expense'])
        type = self.type(nature = nature)

        transaction = {'clientID': clientID,
                       'time': time,
                       'amount': amount,
                       'nature': nature,
                       'type': type}
        return transaction

    def transfer(self) -> dict:
        transaction = self.transaction()
        transfer = self.transaction(transaction = transaction)
        return transfer

    def time(self) -> str:
        years = [2019, 2020, 2021, 2022]
        seed = randint(1, 41)
        floor = seed // 12
        year = years[floor]
        month = (seed % 12) + 1
        if month == 2: day = randint(1, 28)
        else: day = randint(1, 30)
        hour, minutes, seconds = randint(0, 23), randint(0, 59), randint(0, 59)

        return f'{year}-{month}-{day} {hour}:{minutes}:{seconds}'

    def type(self, nature: str) -> str:
        income = ['wages', 'deposit', 'allowance', 'interest', 'benefits', 'sales', 'operating', 'exceptional', 'services', 'royalties']
        expense = ['personal', 'bills', 'deposit', 'application', 'leasing', 'wages', 'bills', 'exceptional', 'contract', 'purchases']

        match nature:
            case 'income': return choice(income)
            case 'expense': return choice(expense)

class New:

    def __init__(self) -> None:
        self.connection = MySQL().connect('contabyx')

    def client(self, nature: str) -> None:
        new_client = Random().client(nature = nature)
        query = f'''
                CALL new_client_{nature} 
                (
                    '{new_client.get('name')}', 
                    '{new_client.get('document').upper()}', 
                    {new_client.get('number')}
                )
                '''
        Query().execute(connection = self.connection, query = query)

    def transaction(self) -> None:
        transaction = Random().transaction()
        query = f'''
                CALL new_transaction_{transaction.get('nature')}
                (
                    {transaction.get('clientID')},
                    {transaction.get('amount')},
                    '{transaction.get('type')}',
                    '{transaction.get('time')}'
                )
                '''
        Query().execute(connection = self.connection, query = query)

    def transfer(self) -> None:
        transfer = Random().transfer()
        query = f'''
                CALL new_transfer
                (
                    {transfer.get('clientID')},
                    {transfer.get('clientID_to')},
                    {transfer.get('amount')},
                    '{transfer.get('type')}',
                    '{transfer.get('time')}'
                )
                '''
        Query().execute(connection = self.connection, query = query)

class Batch:

    def __init__(self) -> None:
        pass

    def insert(self, clients: list, transactions: int):
        for _ in range(clients[0]):
            New().client('natural')

        for _ in range(clients[1]):
            New().client('legal')

        for _ in range(transactions):
            New().transaction()
            New().transfer()