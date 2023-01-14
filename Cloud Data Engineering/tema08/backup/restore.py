import os, pathlib, dotenv

class Main():

    def __init__(self):
        self.backup_path = os.path.join(pathlib.Path(os.path.dirname(__file__)), 'backups')
        self.backup_file = max(os.listdir(self.backup_path), key=lambda f: os.path.getctime("{}/{}".format(self.backup_path, f)))
        self.file_path = os.path.join(self.backup_path, self.backup_file)
        self.container_copy()
        self.set_password()
        self.restore()

    def container_copy(self):
        os.system('docker exec sqlserver mkdir -p /var/opt/mssql/restores')
        os.system('docker cp {} "sqlserver:/var/opt/mssql/restores/{}"'.format(self.file_path, self.backup_file))

    def set_password(self):
        dotenv_path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent.absolute(), 'config', '.env')
        dotenv.load_dotenv(dotenv_path = dotenv_path)
        self.password = os.getenv('PASSWORD')

    def restore(self):
        os.system('docker exec -it sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P {} -Q "RESTORE DATABASE [contabyx] FROM DISK = N\'/var/opt/mssql/restores/{}\' WITH FILE = 1, NOUNLOAD, REPLACE, RECOVERY, STATS = 5"'.format(self.password, self.backup_file))

    def clean_up(self):
        os.system('docker exec sqlserver rm -rf /var/opt/mssql/backups/{}.bak'.format(self.backup_file))

if __name__ == '__main__':
    Main()