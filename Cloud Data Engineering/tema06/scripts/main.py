from database import create, insert
from generate.inserts import Client, Transaction

def main():
    create.main()
    Client().new(50, 10)
    insert.main('clients.sql')
    Transaction().new(250, 250, 250)
    insert.main('transactions.sql')

if __name__ == '__main__':
    main()