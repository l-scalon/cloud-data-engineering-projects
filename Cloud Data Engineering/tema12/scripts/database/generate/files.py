import csv, os, absolute
from pathlib import Path
from database.connect import MySQL
from database.execute import Query
from database.select import Table

class Data:

    def __init__(self) -> None:
        self.connection = MySQL().connect('contabyx')

    def extract(self) -> None:
        query = '''
                SELECT table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                AND table_schema = 'contabyx'
                '''
        tables = Query().execute(connection = self.connection, query = query)
        for row in tables:
            table = Table().select(row[0])
            self.write_to_file(table, row[0])

    def write_to_file(self, table, name):
        data_path = os.path.join(Path(absolute.path()).parent.absolute(), 'data')
        if not os.path.exists(data_path): os.mkdir(data_path)
        with open(f'{os.path.join(data_path, name)}.txt', 'w', encoding = 'utf-8', newline = '') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerows(table)