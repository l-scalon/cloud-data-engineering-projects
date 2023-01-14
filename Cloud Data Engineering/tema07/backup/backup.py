import os
from dotenv import load_dotenv
from pathlib import Path

def get_passwd():
    dotenv_path = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), 'config', '.env')
    load_dotenv(dotenv_path = dotenv_path)
    return os.getenv('DATABASE_SERVER_PASSWORD')

def main():
    os.system('CALL backup.bat {}'.format(get_passwd()))

if __name__ == '__main__':
    main()