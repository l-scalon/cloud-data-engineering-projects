from data.file import Read
from database.query import Select, Insert

class Data:

    def __init__(self) -> None:
        pass

    def insert(self, connection, schema: str):
        table_names = Select().table_names(connection = connection, schema = schema)
        table_names = [table_names[0], table_names[1], table_names[2], table_names[3], table_names[4], table_names[8], table_names[6], table_names[5], table_names[7]]
        for table_name in table_names:
            raw_values = list(Read().read(file_name = table_name, sub_dir = 'tables'))
            header = header = ','.join([value for value in raw_values[0]])
            list_values = raw_values[1:]
            chunksize = 10**5

            while len(list_values) > (chunksize):
                sliced_values = list_values[0:chunksize]
                tuple_values = list(map(tuple, sliced_values))
                values = ','.join([str(value) for value in tuple_values])
                Insert().execute(connection = connection, table = table_name, columns = header, values = values)
                list_values = list_values[chunksize:]

            tuple_values = list(map(tuple, list_values))
            values = ','.join([str(value) for value in tuple_values])
            Insert().execute(connection = connection, table = table_name, columns = header, values = values)