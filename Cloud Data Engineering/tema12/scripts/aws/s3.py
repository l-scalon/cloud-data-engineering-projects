import os, absolute
from database.variables import Variable as env
from pathlib import Path
from boto3 import client, resource

class Upload:

    def __init__(self) -> None:
        self.s3 = client('s3')

    def directory(self, source: str, target: str) -> None:
        os.system(f'aws s3 sync {source} {target}')

    def file(self, source: str, target: str, object: str) -> None:
        self.s3.upload_file(source, target, object)

    def data(self, source = None, target = None) -> None:
        if source == None: source = os.path.join(Path(absolute.path()).parent.absolute(), 'data')
        if target == None: target = f's3://{env().get("BUCKET")}/{env().get("KEY")}/data/'
        self.directory(source, target)

class Replicate:

    def __init__(self) -> None:
        self.s3 = resource('s3')

    def file(self, source_bucket: str, source_object: str, target_bucket: str, target_object: str) -> None:
        source = {'Bucket': source_bucket,
                  'Key': source_object}
        self.s3.meta.client.copy(source, target_bucket, target_object)