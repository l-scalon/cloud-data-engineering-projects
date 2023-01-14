from database.connect import MongoDB

class Client():

    def __init__(self):
        self.database = MongoDB().get_database('contabyx')

    def delete(self, clientID):
        collection = self.database['Clients']
        collection.delete_one({"_id": clientID})
        self.cascade_transaction(clientID)
        
    def cascade_transaction(self, clientID):
        collection = self.database['Transactions']
        transactions = collection.find({"client": clientID})
        for transaction in transactions:
            transfer = transaction.get('transfer_counterpart')
            collection.update_one({"transfer_counterpart": transfer}, {"$unset":{"transfer_counterpart" : ""}})
            collection.delete_one({"_id": transaction.get("_id")})
