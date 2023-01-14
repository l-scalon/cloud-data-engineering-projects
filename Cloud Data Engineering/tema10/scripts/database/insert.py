from datetime import datetime
from bson import ObjectId
from database.document import Client, Transaction
from database.connect import MongoDB

class Document():

    def __init__(self):
        pass

    def insert(self, collection, item: dict or list) -> None:
        if type(item) == dict: collection.insert_one(item)
        if type(item) == list: collection.insert_many(item)

class New_Client(Document):

    def __init__(self):
        self.database = MongoDB().get_database('contabyx')

    def insert(self, client: Client):
        collection = self.database['Clients']
        super().insert(collection, client.build())
        return client.id

class New_Transaction(Document):

    def __init__(self):
        self.database = MongoDB().get_database('contabyx')

    def insert(self, transaction: Transaction):
        collection = self.database['Transactions']
        super().insert(collection, transaction.build())
        return transaction.id

class New_Transfer(New_Transaction):

    def __init__(self):
        super().__init__()

    def insert(self, from_clientID: ObjectId, to_clientID: ObjectId, type: str, time: datetime, amount: float):
        income_transactionID = ObjectId()
        expense_transaction = Transaction(clientID = from_clientID, nature = 'expense', type = type, time = time, amount = amount, counterpart_id = income_transactionID)
        expense_transactionID = super().insert(expense_transaction)
        income_transaction = Transaction(id = income_transactionID, clientID = to_clientID, nature = 'income', type = type, time = time, amount = amount, counterpart_id = expense_transactionID)
        expense_transactionID = super().insert(income_transaction)

    
class New_Document(Document):

    def __init__(self):
        self.database = MongoDB().get_database('contabyx')
    
    def insert(self, clientID, document: tuple):
        collection = self.database['Clients']
        client = collection.find_one({"_id": clientID})
        documents = client['documents']
        documents[document[0]] = document[1]
        collection.update_one({"_id": clientID}, {"$set":{'documents': documents}})