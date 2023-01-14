import logging
from time import sleep
from database.variables import Variable as env
from boto3 import client
from os import system

class Redshift:

    def __init__(self) -> None:
        self.logger = logging.getLogger('redshift')
        logging.basicConfig(level = logging.INFO)

    def __copy(self, table, uri):
        from database.query import Redshift as rs
        query = f'''
                copy {table} from '{uri}'
                iam_role default
                delimiter ','
                removequotes
                emptyasnull
                blanksasnull;
                '''
        id = rs().execute(database = env().get('DATABASE'), cluster = env().get('CLUSTER'), 
                            dbuser = env().get('DBUSER'), query = query)
        return id


    def copy_from_s3_to_redshift(self, connection, schema: str, key = None):
        from database.query import Select
        table_names = Select().table_names(connection = connection, schema = schema)
        qualified_names = []
        files = []
        for table_name in table_names:
            qualified_name = f'{schema}.{table_name}'
            qualified_names.append(qualified_name)
            files.append(str(table_name))

        for table, file in zip(qualified_names, files):
            if key: uri = f's3://{env().get("BUCKET")}/{env().get(f"{key}")}/{file}.csv'
            else: uri = f's3://{env().get("BUCKET")}/{env().get(f"KEY")}/{file}.csv/{file}.csv'
            self.__copy(table = table, uri = uri)

class S3:

    def __init__(self) -> None:
        self.s3 = client('s3')

    def sync_directory(self, source: str, target: str, delete = False) -> None:
        if not delete: system(f'aws s3 sync {source} {target}')
        else: system(f'aws s3 sync {source} {target} --delete')

    def upload_file(self, source: str, target: str, object: str) -> None:
        self.s3.upload_file(source, target, object)

    def sync_from_local_to_s3(self, source: str, key = None, delete = False) -> None:
        if not key: key = 'KEY'
        target = f's3://{env().get("BUCKET")}/{env().get(f"{key}")}'
        self.sync_directory(source = source, target = target, delete = delete)

class Athena:

    def __init__(self) -> None:
        self.athena = client('athena')

    def execute_query(self, query: str, database: str) -> dict:
        response = self.athena.start_query_execution(
            QueryString = query,
            QueryExecutionContext = {
                'Database': f'{database}',
            },
            ResultConfiguration = {
                'OutputLocation': f's3://{env().get("BUCKET")}/{env().get(f"ATHENA")}',
            },
        )
        return response

    def get_results(self, query_id: str, tries = 30) -> list:
        while tries > 0:
            try:
                response = self.athena.get_query_results(
                    QueryExecutionId = f'{query_id}',
                )
            except: sleep(2)
            finally: tries -= 1
        return response
