from datetime import datetime, timedelta
from random import randint, choice, uniform
from faker import Faker
from database.connect import MySQL
from database.select import Client as id, Document as type, Transaction as transtype
from database.execute import Query

class Random:

    def __init__(self) -> None:
        self.fake = Faker(locale = 'pt_BR')

    def documentType(self, nature: str, document: str) -> dict:
        match nature:
            case 'natural': fullname = 'Lorem Ipsum Dolor'.split()
            case 'legal': fullname = 'Lorem Ipsum Dolor Sit'.split()
        for i in range(len(document)):
            word = list(fullname[i])
            word[0] = document[i]
            word = "".join(word)
            fullname[i] = word
        fullname = " ".join(fullname)
        return {'initials': document, 'fullname': fullname, 'type': nature}

    def client(self, nature: str) -> dict:
        match nature:
            case 'natural':
                name = self.fake.name()
                document = self.fake.lexify(text = '???').upper()
                number = self.fake.numerify(text = '##########')
            case 'legal':
                name = self.fake.company()
                document = self.fake.lexify(text = '????').upper()
                number = self.fake.numerify(text = '##########')

        document_type = type().typeID(document)
        if document_type == None: document_type = New().document_type(nature, document)
        return {'name': name, 'document_type': document_type, 'number': number}

    def transaction(self, nature: str, transaction = None,) -> dict:
        if not transaction == None:
            transaction['clientID_to'] = randint(id().min(), id().max())
            return transaction

        clientID = randint(id().min(), id().max())
        amount = round(uniform(500, 50000), 2)
        type = self.type(nature = nature)

        transaction_type, tax_type = self.transaction_and_tax_type(nature, type)

        transaction = {'clientID': clientID,
                       'amount': amount,
                       'typeID': transaction_type,
                       'taxTypeID': tax_type,
                       'nature': nature,
                       'type': type}
        return transaction

    def transaction_and_tax_type(self, nature: int, type: int):
        transaction_type = transtype().typeID(nature, type)
        if transaction_type == None: 
            transaction_type = New().transaction_type(nature, type)
            New().tax_type(transaction_type)
        tax_type = transtype().taxID(transaction_type)
        return transaction_type, tax_type

    def transfer(self) -> dict:
        transaction = self.transaction(nature = 'expense')
        transfer = self.transaction(transaction = transaction, nature = 'expense')

        transaction_type, tax_type = self.transaction_and_tax_type('income', transfer.get('type'))
        transfer['counter_nature'] = 'income'
        transfer['counter_typeID'] = transaction_type
        transfer['counter_taxTypeID'] = tax_type
        return transfer

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
                INSERT INTO Clients (`type`, `name`)
                    VALUES ('{nature}', 
                            '{new_client.get('name')}');
                '''
        Query().execute(connection = self.connection, query = query)
        query = f'''
                INSERT INTO Documents (clientID, `documentTypeID`, `number`)
                    VALUES ({id().max()}, 
                            {new_client.get('document_type')},
                            {new_client.get('number')});
                '''
        Query().execute(connection = self.connection, query = query)

    def transaction(self, fake_time: datetime, transaction, nature) -> None:
        transaction = Random().transaction(nature) if transaction == None else transaction
        time = fake_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        
        query = f'''
                INSERT INTO Transactions (clientID, typeID, `time`, amount)
                    VALUES (
                        {transaction.get('clientID')},
                        {transaction.get('typeID')},
                        '{time}',
                        {transaction.get('amount')}
                    )
                '''
        Query().execute(connection = self.connection, query = query)

        fee = transtype().rate(transaction.get('taxTypeID')) * transaction.get('amount')

        query = f'''
                INSERT INTO Tax (transactionID, taxTypeID, fee)
                    VALUES (
                        {transtype().max()},
                        {transaction.get('taxTypeID')},
                        {fee}
                    )
                '''
        Query().execute(connection = self.connection, query = query)

    def transfer(self, fake_time: datetime) -> None:
        transfer = Random().transfer()
        New().transaction(fake_time, transfer, None)

        query = f'''
                INSERT INTO Transfers ({transfer.get('nature')}_transactionID)
                    VALUES ({transtype().max()})
                '''
        Query().execute(connection = self.connection, query = query)

        transfer['clientID'] = transfer.get('clientID_to')
        transfer['typeID'] = transfer.get('counter_typeID')
        transfer['taxTypeID'] = transfer.get('counter_taxTypeID')
        New().transaction(fake_time, transfer, None)

        query = f'''
                UPDATE Transfers 
                    SET {transfer.get('counter_nature')}_transactionID = {transtype().max()}
                    WHERE transferID = {transtype().max_transfer()}
                '''
        Query().execute(connection = self.connection, query = query)

    def document_type(self, nature: str, document: str) -> int:
        document_type = Random().documentType(nature, document)
        query = f'''
                INSERT INTO DocumentTypes (`initials`, `fullname`, `type`)
                    VALUES ('{document_type.get('initials')}',
                            '{document_type.get('fullname')}',
                            '{document_type.get('type')}');
                '''
        Query().execute(connection = self.connection, query = query)
        return type().typeID(document)

    def transaction_type(self, nature: str, type: str) -> int:
        query = f'''
                INSERT INTO TransactionTypes (`nature`, `transactionType`)
                VALUES ('{nature}', '{type}');
                '''
        Query().execute(connection = self.connection, query = query)
        return transtype().typeID(nature, type)

    def tax_type(self, transaction_type: int) -> int:
        rate = round(uniform(0.001, 0.1), 3)
        query = f'''
                INSERT INTO TaxType (typeID, rate)
                    VALUES (
                        {transaction_type},
                        {rate}
                    )
                '''
        Query().execute(connection = self.connection, query = query)
        return transtype().taxID(transaction_type)

class Batch:

    def __init__(self) -> None:
        self.fake_time = datetime(2015, 7, 1, 0, 0, 0, 0)

    def set_fake_time(self, last_time: datetime) -> datetime:
        fake_time = last_time + timedelta(minutes = 4.8)
        return fake_time

    def insert(self, days: int):
        inserts = days * 100
        for i in range(inserts):
            if (i % 500) == 0: New().client('natural')
            if (i % 5000) == 0: New().client('legal')
            New().transaction(self.fake_time, transaction = None, nature = 'income')
            self.fake_time = self.set_fake_time(self.fake_time)
            New().transaction(self.fake_time, transaction = None, nature = 'expense')
            self.fake_time = self.set_fake_time(self.fake_time)
            New().transfer(self.fake_time)
            self.fake_time = self.set_fake_time(self.fake_time)