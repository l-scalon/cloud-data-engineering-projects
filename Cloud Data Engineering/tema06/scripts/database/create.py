from database import server
from database.query import Query
import os, absolute
from pathlib import Path

class Create:

    def __init__(self):
        self.server_connection = server.connect()
        self.create_path = os.path.join(Path(absolute.path()).parent.absolute(), 'SQL', 'CREATE')
    
    def database_connection(self):
        return server.connect('contabyx')

    def execute(self):
        query_dirs = ['SCHEMA', 'FUNCTIONS', 'PROCEDURES', 'VIEWS']
        for query_dir in query_dirs:
            execute_dir = os.path.join(self.create_path, query_dir)
            for filename in os.listdir(execute_dir):
                file = os.path.join(execute_dir, filename)
                try:
                    Query().file(file, self.server_connection)
                except:
                    Query().file(file, self.database_connection())

def main():
    Create().execute()
