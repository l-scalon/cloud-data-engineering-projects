import mysql.connector as server
from dotenv import load_dotenv
import os, absolute
from pathlib import Path

def get_passwd():
    dotenv_path = os.path.join(Path(absolute.path()).parent.absolute(), 'config', '.env')
    load_dotenv(dotenv_path = dotenv_path)
    return os.getenv('DATABASE_SERVER_PASSWORD')

def connect(database:str = None):
    connection = server.connect(host = 'localhost', user = 'root', passwd = '{}'.format(get_passwd()), database = database, autocommit = True)
    connection.set_charset_collation(charset = 'utf8mb4', collation = 'utf8mb4_0900_ai_ci')
    return connection