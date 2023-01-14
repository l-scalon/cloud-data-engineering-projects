from random import randint
from time import sleep
from database import create
from generate.inserts import Client, Transaction

def recurrent_insert():
    print('Starting recurrent INSERTS, press Ctrl+Z to stop...')
    while True:
        Client().new(randint(0, 10), randint(0, 2))
        Transaction().new(randint(0, 25), randint(0, 25), randint(0, 25))
        sleep(randint(300, 600))

def main():
    create.main()
    Client().new(50, 10)
    Transaction().new(250, 250, 250)
    recurrent_insert()

if __name__ == '__main__':
    main()