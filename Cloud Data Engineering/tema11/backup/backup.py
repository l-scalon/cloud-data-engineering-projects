import os, datetime, dotenv
from datetime import datetime

class Main():

    def __init__(self):
        self.create_directory()
        self.set_name()
        self.set_password()
        self.backup()
        self.clean_up()

    def create_directory(self):
        backup_path = os.path.join(os.path.dirname(__file__), 'backups')
        if not os.path.exists(backup_path): os.makedirs(backup_path)
        self.backup_path = backup_path

    def set_name(self):
        now = datetime.now()
        date_and_time = now.strftime('%Y%m%d%H%M%S')
        self.file_name = 'contabyx{}.sql'.format(date_and_time)

    def set_password(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        dotenv.load_dotenv(dotenv_path = dotenv_path)
        self.password = os.getenv('PASSWORD')

    def backup(self):
        os.system('sudo docker exec mysql /usr/bin/mysqldump -u root --password={} --default-character-set=utf8 --skip-set-charset --skip-add-drop-table --no-create-info --insert-ignore contabyx > {}'.format(self.password, os.path.join(self.backup_path, self.file_name)))
        os.system('sudo chown -R ec2-user {}'.format(os.path.join(self.backup_path, self.file_name)))

    def clean_up(self):
        count = len(os.listdir(self.backup_path))
        while count > 3:
            oldest = min(os.listdir(self.backup_path), key=lambda f: os.path.getctime('{}/{}'.format(self.backup_path, f)))
            os.remove(os.path.join(self.backup_path, oldest))
            count = len(os.listdir(self.backup_path))

if __name__ == '__main__':
    Main()