import os, pathlib, dotenv

class Main():

    def __init__(self):
        self.backup_path = os.path.join(pathlib.Path(os.path.dirname(__file__)), 'backups')
        self.last_backup = max(os.listdir(self.backup_path), key=lambda f: os.path.getctime(f"{self.backup_path}/{f}"))
        self.container_copy()
        self.restore()

    def container_copy(self):
        os.system('docker exec mongodb mkdir -p /dump/contabyx/')
        os.system(f'docker cp {os.path.join(self.backup_path, self.last_backup)}/. mongodb:/dump/contabyx/.')

    def restore(self):
        os.system('docker exec mongodb mongorestore --uri="mongodb://localhost:27017" /dump/')

if __name__ == '__main__':
    Main()