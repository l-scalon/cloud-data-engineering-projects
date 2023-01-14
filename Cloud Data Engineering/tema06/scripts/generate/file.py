import os, absolute
from pathlib import Path

class File():

    def __init__(self, name:str):
        self.path = os.path.join(Path(absolute.path()).parent.absolute(), 'SQL', 'INSERT')
        self.file = os.path.join(self.path, '{}.sql'.format(name))

    def new(self):
        if not os.path.exists(self.path): os.mkdir(os.path.join(self.path))
        if not os.path.exists(self.file): open(self.file, 'w')

    def write(self, query:str):
        self.new()
        with open(self.file, 'a', encoding = 'utf-8') as file:
            file.write(query)