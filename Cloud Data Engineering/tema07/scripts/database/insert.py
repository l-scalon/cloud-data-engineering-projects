from database import server
from database.query import Query
import os, absolute
from pathlib import Path

class Insert():

    def database_connection(self):
        return server.connect('contabyx')

    def file(self, file:str):
        insert_path = os.path.join(Path(absolute.path()).parent.absolute(), 'SQL', 'INSERT')
        file_path = os.path.join(insert_path, file)
        Query().file(file_path, self.database_connection())

    def statement(self, statement:str):
        Query().statement(statement, self.database_connection())