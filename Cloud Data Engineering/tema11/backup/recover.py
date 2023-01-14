import os

import dotenv

class Main():
    
    def __init__(self) -> None:
        self.set_backup_path()
        self.set_backup_file()
        self.set_password()
        self.restore()

    def set_backup_path(self):
        self.backup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')

    def set_backup_file(self):
        self.backup_file = max(os.listdir(self.backup_path), key=lambda f: os.path.getctime("{}/{}".format(self.backup_path, f)))
        self.file_path = os.path.join(self.backup_path, self.backup_file)

    def set_password(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        dotenv.load_dotenv(dotenv_path = dotenv_path)
        self.password = os.getenv('PASSWORD')

    def restore(self):
        os.system('cat {} | docker exec -i mysql /usr/bin/mysql -u root --password={} --default-character-set=utf8 contabyx'.format(self.file_path, self.password))

if __name__ == '__main__':
    Main()