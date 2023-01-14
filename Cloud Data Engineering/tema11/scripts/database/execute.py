import os

class Query:

    def __init__(self) -> None:
        pass

    def execute(self, connection, query: str):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

class File(Query):

    def __init__(self) -> None:
        pass

    def execute(self, connection, file):
        with open(file = file, mode = 'r', encoding = 'utf-8') as f:
            query = f.read()
            super().execute(connection = connection, query = query)

class Directory(File):

    def __init__(self) -> None:
        pass
    
    def execute(self, connection, path):
        for filename in os.listdir(path):
            file = os.path.join(path, filename)
            super().execute(connection = connection, file = file)