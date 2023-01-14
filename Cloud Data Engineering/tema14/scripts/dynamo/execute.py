import boto3

class Query:

    def __init__(self) -> None:
        self.client = boto3.client('dynamodb')

    def put_item(self, table: str, item: dict):
        response = self.client.put_item(
            TableName = table,
            Item = item)
        return response