import mysql.connector as mysql
import pyodbc, os, pathlib, absolute
from dotenv import load_dotenv

class New():

    def __init__(self):
        self.dotenv_path = os.path.join(pathlib.Path(absolute.path()).parent.absolute(), 'config', '.env')
        self.server, self.database, self.username, self.password = self.get_info()
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        self.cursor = self.cnxn.cursor()

    def get_info(self):
        load_dotenv(dotenv_path = self.dotenv_path)
        return os.getenv('SERVER'), os.getenv('DATABASE'), os.getenv('DBUSERNAME'), os.getenv('PASSWORD')

class Old():
    
    def __init__(self):
        self.dotenv_path = os.path.join(pathlib.Path(absolute.path()).parent.absolute(), 'config', '.env')
        self.password, self.database = self.get_info()
        self.cnxn = mysql.connect(host = 'localhost', user = 'root', passwd = '{}'.format(self.password), database = self.database)
        self.cursor = self.cnxn.cursor()

    def get_info(self):
        load_dotenv(dotenv_path = self.dotenv_path)
        return os.getenv('OLD_PASSWORD'), os.getenv('DATABASE')