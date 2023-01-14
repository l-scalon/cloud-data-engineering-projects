import os, sys
from pathlib import Path
sys.path.append(os.path.join(Path(Path(os.path.dirname(__file__)).parent.absolute()).parent.absolute(), 'scripts'))
from database import create

def main():
    create.main()

if __name__ == '__main__':
    main()