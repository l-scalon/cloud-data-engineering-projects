from dotenv import load_dotenv
import os, absolute

class Variable:

    def __init__(self) -> None:
        self.config_path = os.path.join(absolute.path(), 'config')

    def get(self, variable: str) -> str:
        load_dotenv(dotenv_path = os.path.join(self.config_path, '.env'))
        return os.getenv(variable)