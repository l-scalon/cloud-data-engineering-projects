from database.connect import MySQL
from database.query import Extract
from data.file import File
from aws.aws import S3, Redshift

def main() -> None:
    mysql = MySQL().connect(database = 'cinemyx')
    Extract().new_entries_to_csv(connection = mysql, schema = 'cinemyx')
    S3().sync_from_local_to_s3(source = File().data_path(sub_dir = 'tables'))
    S3().sync_from_local_to_s3(source = File().data_path(sub_dir = 'new_entries'), key = 'KEY_NEW_ENTRIES', delete = True)
    Redshift().copy_from_s3_to_redshift(connection = mysql, schema = 'cinemyx', key = 'KEY_NEW_ENTRIES')

if __name__ == '__main__':
    main()