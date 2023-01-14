import os, datetime, pathlib, dotenv
from datetime import datetime

class Main():

    def __init__(self):
        self.create_directory()
        self.set_name()
        self.set_password()
        self.backup()
        self.host_copy()
        self.clean_up()

    def create_directory(self):
        path = os.path.join(os.path.dirname(__file__), 'backups')
        if not os.path.exists(path): os.makedirs(path)
        self.backup_path = path

    def set_name(self):
        now = datetime.now()
        date_and_time = now.strftime("%Y%m%d%H%M%S")
        file_name = 'contabyx{}.bak'.format(date_and_time)
        self.file_name = file_name

    def set_password(self):
        dotenv_path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent.absolute(), 'config', '.env')
        dotenv.load_dotenv(dotenv_path = dotenv_path)
        self.password = os.getenv('PASSWORD')

    def backup(self):
        os.system('docker exec -it sqlserver /opt/mssql-tools/bin/sqlcmd -b -V16 -S localhost -U SA -P {} -Q "BACKUP DATABASE [contabyx] TO DISK = N\'/var/opt/mssql/backups/{}.bak\' with NOFORMAT, NOINIT, NAME = \'{}-full\', SKIP, NOREWIND, NOUNLOAD, STATS = 10"'.format(self.password, self.file_name, self.file_name))

    def host_copy(self):
        os.system('docker cp sqlserver:/var/opt/mssql/backups/{}.bak {}/{}'.format(self.file_name, self.backup_path, self.file_name))

    def clean_up(self):
        os.system('docker exec sqlserver rm -rf /var/opt/mssql/backups/{}.bak'.format(self.file_name))
        count = len(os.listdir(self.backup_path))
        while count > 3:
            oldest = min(os.listdir(self.backup_path), key=lambda f: os.path.getctime("{}/{}".format(self.backup_path, f)))
            os.remove(os.path.join(self.backup_path, oldest))
            count = len(os.listdir(self.backup_path))

if __name__ == '__main__':
    Main()