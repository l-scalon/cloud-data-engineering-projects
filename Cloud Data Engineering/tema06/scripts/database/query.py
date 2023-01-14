class Query:
    def execute(self, query, connection):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def file(self, query_path, connection):
        with open(query_path, 'r') as file:
            query = file.read()
            self.execute(query, connection)