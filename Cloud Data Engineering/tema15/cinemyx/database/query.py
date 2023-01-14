from datetime import time
from data.file import File, Write
from aws.aws import Athena
import boto3

class Query:

    def __init__(self) -> None:
        pass

    def execute(self, connection, query: str) -> list:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

class Select(Query):

    def __init__(self) -> None:
        super().__init__()

    def execute(self, connection, table: str, columns = '*', arguments = ';') -> list:
        query = f"SELECT {columns} FROM {table} {arguments}"
        return super().execute(connection, query)

    def table_names(self, connection, schema: str) -> list:
        columns, table = 'table_name', 'information_schema.tables'
        arguments = f"WHERE table_type = 'BASE TABLE' AND table_schema = '{schema}';"
        table_names = []
        tables = self.execute(connection = connection, table = table, columns = columns, arguments = arguments)
        for table in tables:
            table_names.append(table[0])
        return table_names

    def table(self, connection, table: str):
        return self.execute(connection = connection, table = table, arguments = 'ORDER BY 1;')

class Extract(Select):

    def __init__(self) -> None:
        super().__init__()

    def tables_to_csv(self, connection, schema: str):
        table_names = super().table_names(connection = connection, schema = schema)
        for table_name in table_names:
            self.table_to_csv(connection = connection, table_name = table_name)

    def table_to_csv(self, connection, table_name: str):
        table = super().table(connection = connection, table = table_name)
        Write().write(file_name = table_name, sub_dir = 'tables', rows = table, file_name_dir = True)

    def new_entries_to_csv(self, connection, schema: str):
        table_names = super().table_names(connection = connection, schema = schema)
        for table_name in table_names:
            response = Athena().execute_query(query = f"SELECT MAX(col0) FROM {table_name}_csv", database = f'{schema}-csv')
            result = Athena().get_results(query_id = response.get('QueryExecutionId'))

            data_on_athena_max_id = result['ResultSet']['Rows'][1]['Data'][0]['VarCharValue']
            data_on_athena_max_id = int(data_on_athena_max_id)
            data_on_mysql_max_id = super().execute(connection = connection, table = table_name, columns = f'MAX({table_name}id)')
            data_on_mysql_max_id = data_on_mysql_max_id[0][0]

            if int(data_on_mysql_max_id) > int(data_on_athena_max_id):
                arguments = f"WHERE {table_name}id BETWEEN {(data_on_athena_max_id + 1)} AND {data_on_mysql_max_id};"
                new_entries = super().execute(connection = connection, table = table_name, arguments = arguments)
                Write().write(file_name = table_name, sub_dir = 'new_entries', rows = new_entries)
                for new_entry in new_entries:
                        Write().append(file_name = table_name, sub_dir = 'tables', row = new_entry, file_name_dir = True)
            else: File().delete(sub_dir = 'new_entries', file_name = table_name)
                
class Insert(Query):

    def __init__(self) -> None:
        super().__init__()

    def execute(self, connection, table: str, columns: tuple, values: list) -> None:
        query = f"INSERT INTO {table}({columns}) VALUES {values};"
        super().execute(connection = connection, query = query)

class Redshift:

    def execute(self, database: str, cluster: str, dbuser: str, query: str) -> str:
        client = boto3.client('redshift-data')
        response = client.execute_statement(
            Database = database,
            ClusterIdentifier = cluster,
            DbUser = dbuser,
            Sql = query)
        return response['Id']

    def fetch(self, id: str, wait: int):
        client = boto3.client('redshift-data')
        for i in range(1, 4):
            try:
                return client.get_statement_result(Id = id)
            except:
                self.logger.info(f"Query not yet finished. Waiting for {wait} second(s). Try: #{i}")
                time.sleep(wait)