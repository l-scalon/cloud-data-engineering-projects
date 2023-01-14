from datetime import date
from boto3 import client
from boto3.dynamodb import types
from logging import getLogger, basicConfig, WARN

class contabyxAPI:

    def __init__(self, aws_access_key_id, aws_secret_access_key) -> None:
        self.dynamo = client('dynamodb',
                        aws_access_key_id = aws_access_key_id,
                        aws_secret_access_key = aws_secret_access_key)
        self.logger = getLogger('contabyxAPI')
        basicConfig(level = WARN)

    def __get_item(self, table: str, key: str, id: int, attr = '') -> dict or None:
        if attr == '':
            response = self.dynamo.get_item(
                TableName = table,
                Key = {f'{key}': {f'N': str(id)}})
        else:
            response = self.dynamo.get_item(
                TableName = table,
                Key = {f'{key}': {f'N': str(id)}},
                AttributesToGet = [attr])
        try: return response['Item']
        except: return None

    def __get_client(self, table: str, id: int, attr = '') -> dict or None:
        if attr != '':
            response = self.__get_item(
                table = f'{table}', 
                key = 'clientid', 
                id = id, 
                attr = attr)
        else:
            response = self.__get_item(
                table = f'{table}', 
                key = 'clientid', 
                id = id)
        if response == None: self.logger.warn(f'Query on table {table} for ID {id} and attribute {attr} returned an empty result.')
        else: response = self.__deserialize(item = response)
        return response
    
    def __deserialize(self, item: dict):
        for key in item.keys():
            item[key] = types.TypeDeserializer().deserialize(item[key])
        return item

    def balance(self, id: int) -> float or None:
        balance = self.__get_client(id = id, table = 'clients_info')
        return float(balance['balance']) if balance != None else None

    def __transactions(self, id: int, nature: str, year = 0, month = 0, full_year = False) -> int or dict:
        if year != 0 and year not in range(2015, date.today().year + 1): 
            raise Exception(f'Year {year} is not within valid range.')
        if year == 0: return int(self.__get_client(id = id, table = 'clients_info')[f'total_{nature}'])
        if month == 0:
            year_dict = self.__get_client(id = id, table = 'clients_info_by_year', attr = str(year))
            if full_year: return year_dict
            try: return int(year_dict[str(year)][f'{nature}'])
            except: return 0
        else:
            if month not in range(1, 13):
                raise Exception(f'Month {month} is not within valid range.')
            else: 
                year_dict = self.__get_client(id = id, table = 'clients_info_by_year', attr = str(year))
                try: return year_dict[str(year)][str(month)][f'{nature}']
                except: return 0

    def income(self, id: int, year = 0, month = 0) -> int:
        return self.__transactions(id = id, year = year, month = month, nature = 'income')
    
    def expense(self, id: int, year = 0, month = 0) -> int:
        return self.__transactions(id = id, year = year, month = month, nature = 'expense')

    def client(self, id: int, return_type = 'total') -> dict:
        if not return_type in ['total', 'by_year', 'by_month']:
            raise Exception(f'{return_type} is not a valid return_type. return_type shoud be one of: total, by_year, by_month')
        client = {}
        client['clientid'] = id
        client['balance'] = self.balance(id = id)
        client['income'] = self.income(id = id)
        client['expense'] = self.expense(id = id)
        if return_type == 'by_year':
            client['years'] = {}
            for year in range(2015, date.today().year + 1):
                year_pair = {}
                year_pair['income'] = self.income(id = id, year = year)
                year_pair['expense'] = self.expense(id = id, year = year)
                client[year] = year_pair
                client['years'].update(client[year])
        elif return_type == 'by_month':
            client['years'] = {}
            for year in range(2015, date.today().year + 1):
                full_year = self.__transactions(id = id, nature = 'by_month', year = year, full_year = True)
                client['years'].update(full_year)
        else: pass
        return client