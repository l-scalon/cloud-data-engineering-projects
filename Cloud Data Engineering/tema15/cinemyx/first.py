from database.connect import MySQL
from database.query import Extract
from data.file import File
from aws.aws import S3, Redshift

def main() -> None:
    mysql = MySQL().connect(database = 'cinemyx')
    Extract().tables_to_csv(connection = mysql, schema = 'cinemyx')
    S3().sync_from_local_to_s3(source = File().data_path(sub_dir = 'tables'))
    Redshift().copy_from_s3_to_redshift(connection = mysql, schema = 'cinemyx')

if __name__ == '__main__':
    main()