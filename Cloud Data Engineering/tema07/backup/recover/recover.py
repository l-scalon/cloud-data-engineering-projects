import os, sys
from dotenv import load_dotenv
from pathlib import Path

class Recover():

    def get_passwd(self):
        dotenv_path = os.path.join(Path(Path(os.path.dirname(__file__)).parent.absolute()).parent.absolute(), 'config', '.env')
        load_dotenv(dotenv_path = dotenv_path)
        return os.getenv('DATABASE_SERVER_PASSWORD')

    def main(self, strategy:str):
        os.system('CALL {}.bat {}'.format(strategy, self.get_passwd()))

if __name__ == '__main__':
    Recover().main('{}'.format(sys.argv[1]))