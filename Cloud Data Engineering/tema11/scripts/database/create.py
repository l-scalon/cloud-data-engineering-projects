from database.execute import Directory
import os, absolute
from pathlib import Path

class Create:

    def __init__(self):
        self.sql_path = os.path.join(Path(absolute.path()).parent.absolute(), 'SQL')

    def object(self, connection, object: str):
        dir = os.path.join(self.sql_path, object)
        Directory().execute(connection = connection, path = dir)
        
    def default(self, connection):
        dirs = ['FUNCTIONS', 'PROCEDURES', 'VIEWS']
        for dir in dirs:
            self.object(connection = connection, object = dir)