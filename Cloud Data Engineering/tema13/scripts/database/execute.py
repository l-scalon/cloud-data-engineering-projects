class Query:

    def __init__(self) -> None:
        pass

    def execute(self, connection, query: str):
        cursor = connection.cursor()
        cursor.execute(query).commit()
        return cursor

class File(Query):

    def __init__(self) -> None:
        pass

    def execute(self, connection, file: str):
        with open(file = file, mode = 'r', encoding = 'utf-8') as f:
            query = f.read()
            cursor = super().execute(connection = connection, query = query)
            return cursor