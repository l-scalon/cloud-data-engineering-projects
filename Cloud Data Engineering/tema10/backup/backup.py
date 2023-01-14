import os, datetime, shutil
from datetime import datetime

class Main():

    def __init__(self):
        self.create_directory()
        self.set_name()
        self.backup()
        self.host_copy()
        self.clean_up()

    def create_directory(self):
        self.backup_path = os.path.join(os.path.dirname(__file__), 'backups')
        if not os.path.exists(self.backup_path): os.makedirs(self.backup_path)

    def set_name(self):
        now = datetime.now()
        date_and_time = now.strftime("%Y%m%d%H%M%S")
        self.dir_name = f'contabyx{date_and_time}'
        self.full_path = os.path.join(self.backup_path, self.dir_name)
        os.makedirs(self.full_path)

    def backup(self):
        os.system('docker exec mongodb mongodump --uri="mongodb://localhost:27017"')

    def host_copy(self):
        os.system(f'docker cp mongodb:/dump/contabyx/. {self.full_path}')

    def clean_up(self):
        count = len(os.listdir(self.backup_path))
        while count > 3:
            oldest = min(os.listdir(self.backup_path), key=lambda f: os.path.getctime(f"{self.backup_path}/{f}"))
            shutil.rmtree(os.path.join(self.backup_path, oldest))
            count = len(os.listdir(self.backup_path))

if __name__ == '__main__':
    Main()