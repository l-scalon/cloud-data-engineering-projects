from time import sleep
import mysql.connector as server
import pyodbc as sqlserver
import os
from database.variables import Variable as env

class MySQL:

    def __init__(self) -> None:
        pass

    def get_host(self) -> str:
        instance = env().get('INSTANCE')
        public_ip = os.popen(f'powershell (Get-EC2Instance -InstanceId {instance}).Instances.PublicIpAddress').read()
        address = public_ip.replace('.', '-').replace('\n', '')
        host = 'ec2-' + f'{address}' + '.us-east-2.compute.amazonaws.com'
        return host

    def reconnect(self):
        instance = env().get('INSTANCE')
        os.system(f'aws ec2 --instance-ids start-instances {instance}')
        sleep(30)

    def connect(self, database: str = None, autocommit = True, tries = 3):
        for _ in range(tries):
            try:
                connection = server.connect(host = self.get_host(), 
                                            user = env().get('USER'), 
                                            passwd = env().get('PASSWORD'), 
                                            database = database, 
                                            autocommit = autocommit, 
                                            ssl_ca = os.path.join(env().config_path, env().get('KEYPAIR')))
                connection.set_charset_collation(charset = 'utf8mb4', collation = 'utf8mb4_0900_ai_ci')
                return connection
            except:
                self.reconnect()

class SQLServer:

    def __init__(self) -> None:
        pass

    def connect(self, database: str = None):
        connection = sqlserver.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + 
                                            env().get('SERVER') + ';DATABASE=' + database + ';UID=' + env().get('DBUSERNAME') + ';PWD=' + env().get('SSPASSWORD'))
        return connection
