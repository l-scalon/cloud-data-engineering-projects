import os, absolute
from pathlib import Path

class Variable:

    def __init__(self) -> None:
        self.parent_path = os.path.join(Path(absolute.path()).parent.absolute())

    def path(self, dir: str, file: str) -> str:
        path = os.path.join(self.parent_path, dir, file)
        return path