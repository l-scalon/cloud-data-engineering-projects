from dynamo.execute import Query as dynamo
from redshift.execute import Query as redshift
import logging, json
from decimal import Decimal
from variables import Variable as env
import boto3.dynamodb.types as types

class Insert:

    def __init__(self) -> None:
        self.logger = logging.getLogger('dynamo')
        logging.basicConfig(level = logging.INFO)

    def clients_info(self, entries = 0):
        columns = ['clientid', 'balance', 'total_income', 'total_expense']
        string_columns = ', '.join(map(str, columns))
        query = f"SELECT {string_columns} from contabyx.clients_info"
        query_id = redshift().execute(
            database = env().get('DATABASE'),
            cluster = env().get('CLUSTER'),
            dbuser = env().get('DBUSER'),
            query = query)
        result = redshift().fetch(id = query_id, wait = 10)
        if entries < 0: raise Exception('entries should be equal or greater than 0.')
        entries = entries if entries > 0 else len(result['Records'] - 1)
        for row in result['Records'][:(entries - 1)]:
            client = {}
            for column, value in zip(columns, row):
                try: value = value['longValue']
                except: value = float(value['stringValue'])
                if not value == 0: client[column] = value
            if len(client.keys()) > 1:
                self.__put_item(table = 'clients_info', item = client)
                self.logger.info(f'Insert client {client["clientid"]} into clients_info: DONE.')

    def clients_info_by_month(self, entries = 0):
        columns = ['clientid', 'year', 'month', 'income', 'expense']
        string_columns = ', '.join(map(str, columns))
        query = f"SELECT {string_columns} from contabyx.clients_info_by_month"
        query_id = redshift().execute(
            database = env().get('DATABASE'),
            cluster = env().get('CLUSTER'),
            dbuser = env().get('DBUSER'),
            query = query)
        result = redshift().fetch(id = query_id, wait = 2)
        if entries < 0: raise Exception('entries should be equal or greater than 0.')
        entries = entries if entries > 0 else len(result['Records'])
        clients = {}
        for row in result['Records'][:(entries - 1)]:
            client_id = row[0]['longValue']
            year = row[1]['longValue']
            month = row[2]['longValue']
            income = row[3]['longValue']
            expense = row[4]['longValue']
            month_pair = {}
            if not income == 0: month_pair['income'] = income
            if not expense == 0: month_pair['expense'] = expense
            if 'income' in month_pair or 'expense' in month_pair:
                month_dict = {month: month_pair}
                year_dict = {year: month_dict}
                if not client_id in clients:
                    clients[client_id] = year_dict
                else:
                    if not year in clients[client_id]:
                        nested_years = clients[client_id]
                        nested_years.update(year_dict)
                        clients[client_id] = nested_years
                    else:
                        nested_year = clients[client_id][year]
                        nested_year.update(month_dict)
                        clients[client_id][year] = nested_year
        for client_id in clients.keys():
            client = {}
            client['clientid'] = client_id
            for year in clients[client_id].keys():
                total_income = 0
                total_expense = 0
                for month in clients[client_id][year].keys():
                    try: total_income += clients[client_id][year][month]['income']
                    except: pass
                    try: total_expense += clients[client_id][year][month]['expense']
                    except: pass
                total = {}
                if total_income != 0: total['income'] = total_income
                if total_expense != 0: total['expense'] = total_expense
                if total_income != 0 or total_expense != 0:
                    clients[client_id][year].update(total)
                    client[year] = clients[client_id][year]
            self.__put_item(table = 'clients_info_by_year', item = client)
            self.logger.info(f'Insert client {client_id} into clients_info_by_year: DONE.')


    def __put_item(self, table: str, item: dict):
        item = json.loads(json.dumps(item), parse_float = Decimal)
        for key in item.keys():
            item[key] = types.TypeSerializer().serialize(item[key])
        dynamo().put_item(table = table, item = item)