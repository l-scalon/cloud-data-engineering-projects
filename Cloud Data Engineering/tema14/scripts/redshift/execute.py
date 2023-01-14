import boto3, logging, time

class Query:

    def __init__(self) -> None:
        self.logger = logging.getLogger('redshift')
        logging.basicConfig(level = logging.INFO)

    def execute(self, database: str, cluster: str, dbuser: str, query: str) -> str:
        client = boto3.client('redshift-data')
        response = client.execute_statement(
            Database = database,
            ClusterIdentifier = cluster,
            DbUser = dbuser,
            Sql = query)
        self.logger.info(f"Query \'{query}\' is being executed. Use query ID to fetch the results.")
        return response['Id']

    def fetch(self, id: str, wait = 5):
        client = boto3.client('redshift-data')
        for i in range(1, 4):
            try:
                return client.get_statement_result(Id = id)
            except:
                self.logger.info(f"Query not yet finished. Waiting for {wait} second(s). Try: #{i}")
                time.sleep(wait)