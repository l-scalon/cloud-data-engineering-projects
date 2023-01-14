from dotenv import load_dotenv
import os, absolute
from pathlib import Path

class Variable:

    def __init__(self) -> None:
        self.config_path = os.path.join(Path(absolute.path()).parent.absolute(), 'config')

    def get(self, variable: str) -> str:
        load_dotenv(dotenv_path = os.path.join(self.config_path, '.env'))
        return os.getenv(variable)