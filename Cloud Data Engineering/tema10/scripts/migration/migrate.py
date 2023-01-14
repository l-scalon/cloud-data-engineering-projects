from migration.prepare import Prepare
from database.document import Client, Transaction
from database.select import SQLServer as query
from database.insert import New_Client, New_Transaction

def main():
    collections = ['Clients', 'Transactions']
    database = Prepare().create_database()
    clients = query().select(table = "contabyx.Clients")
    transactions = query().select(table = "contabyx.Transactions")

    client_ids = Prepare().create_ids(('contabyx.Clients', 'clientID'))
    transaction_ids = Prepare().create_ids(('contabyx.Transactions', 'transactionID'))

    Prepare().create_collections(database, collections)

    for client in clients:

        origin_documents = query().select(table = "contabyx.Documents", optional_clause = f" WHERE clientID = {client[0]}")
        target_documents = {}
        for document in origin_documents:
            target_documents[document[1]] = document[2]

        new_client = Client(id = client_ids.get(client[0]), type = client[1], name = client[2], documents = target_documents)
        New_Client().insert(new_client)

    for transaction in transactions:

        origin_tax = query().select(table = "contabyx.Tax", columns = "rate, fee", optional_clause = f" WHERE transactionID = {transaction[0]}")
        target_tax = {"rate": round(origin_tax[0][0], 2), "fee": round(origin_tax[0][1], 2)}

        try:
            type = query().select(table = "contabyx.TransactionTypes", columns = "transaction_type", optional_clause = f" WHERE transactionID = {transaction[0]}")[0][0]
        except:
            type = None

        new_transaction = Transaction(id = transaction_ids.get(transaction[0]), clientID = client_ids.get(transaction[1]), nature = transaction[2], type = type, time = transaction[3], amount = transaction[4], tax = target_tax)

        match transaction[2]:
            case 'expense': counterpart = "income_transactionID"
            case 'income':  counterpart = "expense_transactionID"
        transfer_result = query().select(table = "contabyx.Transfers", columns = counterpart, optional_clause = f" WHERE {transaction[2]}_transactionID = {transaction[0]}")
        if len(transfer_result) > 0 and isinstance(transfer_result[0][0], int): new_transaction.set_counterpart(transaction_ids.get(transfer_result[0][0]))

        New_Transaction().insert(new_transaction)