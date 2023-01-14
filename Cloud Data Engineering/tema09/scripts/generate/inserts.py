from database import insert
import time

class Batch():

    def __init__(self):
        pass

    def new(self, inserts:list):

        for _ in range(inserts[0]):
            insert.Client().new('natural')

        for _ in range(inserts[1]):
            insert.Client().new('legal')

        for _ in range(inserts[2]):
            insert.Transaction().new('expense')
            insert.Transaction().new('income')
            insert.Transfer().new()

class Recurrent():

    def __init__(self, inserts:list, times:int, sleep:int):
        print('\n-- Starting recurrent inserts for {} times, with an interval of {} seconds each. --\n'.format(times, sleep))
        
        for i in range(times):
            print('STARTING BATCH #{}'.format(i+1))
            Batch().new(inserts)
            print('BATCH DONE.')
            if i + 1 != times:
                print('Sleeping for {} seconds.\n'.format(sleep)) 
                time.sleep(sleep)