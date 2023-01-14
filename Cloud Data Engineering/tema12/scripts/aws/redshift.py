from aws.s3 import Replicate, Upload
import os, absolute, logging
from pathlib import Path
from database.variables import Variable as env

class Copy:

    def __init__(self) -> None:
        log_path = os.path.join(Path(absolute.path()).parent.absolute(), 'logs')
        if not os.path.exists(log_path): os.mkdir(log_path)
        self.redshift_log = os.path.join(log_path, 'redshift.log')
        if not os.path.exists(log_path): os.mkdir(self.redshift_log)
        logging.basicConfig(filename = f'{self.redshift_log}', level = logging.ERROR, format = '%(asctime)s %(levelname)s %(name)s %(message)s')
        self.logger = logging.getLogger(__name__)

    def from_s3_to_redshift(self, connection, table, uri):
        query = f'''
                copy {table} from '{uri}'
                iam_role default
                delimiter ','
                removequotes
                emptyasnull
                blanksasnull;
                '''
        cursor = connection.cursor()
        cursor.execute(query).commit()

    def default(self, connection = None):

        source_bucket = env().get('BUCKET')
        
        tables = ['contabyx.clients',
                  'contabyx.documents',
                  'contabyx.documenttypes',
                  'contabyx.tax',
                  'contabyx.taxtype',
                  'contabyx.transactions',
                  'contabyx.transactiontypes',
                  'contabyx.transfers']

        files = ['Clients',
                 'Documents',
                 'DocumentTypes',
                 'Tax',
                 'TaxType',
                 'Transactions',
                 'TransactionTypes',
                 'Transfers']

        for table, file in zip(tables, files):
            source_object = f'{env().get("KEY")}/data/{file}.txt'
            uri = f's3://{env().get("BUCKET")}/{env().get("KEY")}/data/{file}.txt'
            try:
                self.from_s3_to_redshift(connection = connection, table = table, uri = uri)
                target_object = f'{env().get("KEY")}/processed/{file}.txt'
            except Exception as e:
                connection.rollback()
                target_object = f'{env().get("KEY")}/error/{file}.txt'
                self.logger.exception(e)
            Replicate().file(source_bucket = source_bucket, source_object = source_object, target_bucket = source_bucket, target_object = target_object)
        Upload().file(self.redshift_log, f'{env().get("BUCKET")}', f'{env().get("KEY")}/error/redshift.log')