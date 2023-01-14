import pyodbc, os, pathlib, absolute
from dotenv import load_dotenv
from pymongo import MongoClient

class SQLServer():

    def __init__(self):
        self.dotenv_path = os.path.join(pathlib.Path(absolute.path()).parent.absolute(), 'config', '.env')
        self.server, self.database, self.username, self.password = self.get_info()
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        self.cursor = self.connection.cursor()

    def get_info(self):
        load_dotenv(dotenv_path = self.dotenv_path)
        return os.getenv('SERVER'), os.getenv('DATABASE'), os.getenv('DBUSERNAME'), os.getenv('PASSWORD')

class MongoDB():

    def __init__(self):
        self.connection = "mongodb://localhost:27017"
        self.client = MongoClient(self.connection)

    def get_database(self, database: str):
        return self.client[database]

    def drop_database(self, database: str):
        self.client.drop_database(database)