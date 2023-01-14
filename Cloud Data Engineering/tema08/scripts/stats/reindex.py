from database import server

class Reindex():

    def __init__(self):
        self.reindex()

    def reindex(self):
        tables = ['Clients', 'Documents', 'Tax', 'Transactions', 'Transfers']
        for table in tables:
            info = Index().get_fragmentation_info(table)
            for row in info:
                if row[2] >= 15 and row[2] <= 30: Strategy(row, table).reorganize()
                elif row[2] > 30: Strategy(row, table).rebuild()
                else: pass

class Index():

    def __init__(self):
        pass

    def get_fragmentation_info(self, table):
        query = '''
                SELECT a.index_id, name, avg_fragmentation_in_percent
                    FROM sys.dm_db_index_physical_stats (DB_ID(N'contabyx'),
                    OBJECT_ID(N'contabyx.{}'), NULL, NULL, NULL) AS a
                    JOIN sys.indexes AS b
                        ON a.object_id = b.object_id AND a.index_id = b.index_id;
                '''.format(table)
        cursor = server.New().cursor
        cursor.execute(query)
        info = cursor.fetchall()
        return info

class Strategy():

    def __init__(self, row, table):
        self.row = row
        self.table = table

    def reorganize(self):
        query = 'ALTER INDEX {} ON contabyx.{} REORGANIZE'.format(self.row[1], self.table)
        cursor = server.New().cursor
        cursor.execute(query).commit()

    def rebuild(self):
        query = 'ALTER INDEX {} ON contabyx.{} REBUILD WITH (ONLINE = ON)'.format(self.row[1], self.table)
        cursor = server.New().cursor
        cursor.execute(query).commit()