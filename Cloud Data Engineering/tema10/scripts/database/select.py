from pandas import DataFrame
from database.connect import SQLServer as sql, MongoDB

class Collection():

    def __init__(self):
        pass

    def filter(self, items, columns):
        filtered = []
        for item in items:
            filtered_dict = {key: value for key, value in item.items() if key in columns}
            filtered.append(filtered_dict)
        return filtered

    def select(self, collection, columns = [], dataframed = False):
        items = list(collection.find())
        if len(columns) > 0: items = self.filter(items, columns)
        if dataframed: print(DataFrame(items))
        return items
        
class Document():

    def __init__(self):
        pass

    def by_one_key(self, collection, value, columns = [], key = "_id", dataframed = False):
        items = list(collection.find({key: value}))
        if len(columns) > 0: items = Collection().filter(items, columns)
        if dataframed: print(DataFrame(items))
        return items

    def by_many_keys(self, collection, values: list, columns = [], keys = ["_id"], keyword = "or", dataframed = False):

        if keyword in ['or', 'and']: pass
        else: raise Exception('\"keyword\" must be a valid keyword.') 

        pairs = []
        if len(keys) == len(values):
            for key, value in zip(keys, values):
                pair = {key: value}
                pairs.append(pair)
        elif len(keys) == 1: 
            for value in values:
                pair = {keys[0]: value}
                pairs.append(pair)
        else: raise Exception('Pairs must meet one of two conditions:\n1. Same number of keys and values; OR\n2. Any number of values for just one key.')

        items = list(collection.find({f"${keyword}":pairs}))
        if len(columns) > 0: items = Collection().filter(items, columns)
        if dataframed: print(DataFrame(items))
        return items

class Views():

    def __init__(self):
        self.database = MongoDB().get_database('contabyx')

    def balance(self, clientID, dataframed = False):
        collection = self.database['Transactions']
        transactions = collection.find({"client": clientID})
        balance = 0
        for transaction in transactions:
            if transaction.get('nature') == 'income': balance += transaction.get('amount')
            else: balance -= transaction.get('amount')
        collection = self.database['Clients']
        if dataframed:
            items = Document().by_one_key(collection = collection, value = clientID, columns = ["_id", "name"])
            if len(items) > 0:
                items = items[0]
                items['balance'] = round(balance, 2)
                print(DataFrame(items, index = [0]))
            else: raise Exception('ClientID must be a valid client _id.')
        return items

    def transaction_history(self, clientID, dataframed = False):
        collection = self.database['Transactions']
        transactions = Document().by_one_key(collection = collection, value = clientID, key = 'client', columns = ["_id", "time", "amount", "nature"])
        if len(transactions) > 0:
            history = []
            for transaction in transactions:
                if transaction.get('nature') == 'expense': transaction['amount'] = transaction.get('amount') * -1
                history.append(transaction)
            items = Collection().filter(history, ["_id", "time", "amount"])
            if dataframed: print(DataFrame(items).sort_values(by = 'time'))
            return items
        else: raise Exception('ClientID must be a valid client _id.')

class SQLServer():

    def __init__(self):
        pass

    def select(self, table: str, columns = "*", optional_clause = ";"):
        query = f"SELECT {columns} FROM {table}{optional_clause}"
        cursor = sql().cursor
        cursor.execute(query)
        return cursor.fetchall()