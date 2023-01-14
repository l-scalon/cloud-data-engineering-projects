import os, sys
from pathlib import Path
sys.path.append(os.path.join(Path(Path(os.path.dirname(__file__)).parent.absolute()), 'scripts'))
from database import server
from database.query import Query
from dotenv import load_dotenv

class Server():

    def get_passwd(self):
        dotenv_path = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), 'config', '.env')
        load_dotenv(dotenv_path = dotenv_path)
        return os.getenv('DATABASE_SERVER_PASSWORD')

    def main(self):
        connection = server.connect('contabyx')
        Query().statement('call contabyx.delete_null_from_transfers();', connection)
        os.system('CALL update.bat {}'.format(self.get_passwd()))

if __name__ == '__main__':
    Server().main()