from database import server
from database.query import Query
import os, absolute
from pathlib import Path

def database_connection():
    return server.connect('contabyx')

def main(file:str):
    insert_path = os.path.join(Path(absolute.path()).parent.absolute(), 'SQL', 'INSERT')
    file_path = os.path.join(insert_path, file)
    Query().file(file_path, database_connection())