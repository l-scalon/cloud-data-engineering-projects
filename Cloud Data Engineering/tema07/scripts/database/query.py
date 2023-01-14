class Query:
    def execute(self, query, connection):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def file(self, query_path, connection):
        with open(query_path, 'r', encoding = 'utf-8') as file:
            query = file.read()
            self.execute(query, connection)
    
    def statement(self, statement:str, connection):
        return self.execute(statement, connection)