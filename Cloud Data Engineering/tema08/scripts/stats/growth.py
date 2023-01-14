from database import server

class Projection():

    def __init__(self, growth:float, per_day:int, disk_size:int):
        self.database_size = float(self.get_size())
        self.growth = growth
        self.per_day = per_day
        self.disk_size = float(disk_size * 1000)
        self.growth_per_day = growth * (per_day / 1000)
        self.growth_per_month = float(self.growth_per_day * 30)
        self.months_untill_full = round(((self.disk_size - self.database_size) / self.growth_per_month), 2)

        self.print()

    def get_size(self):
        query = '''
                SELECT 
                    total_size_mb = CAST(SUM(size) * 8. / 1024 AS DECIMAL(8,2))
                    FROM sys.master_files WITH(NOWAIT)
                    WHERE database_id = DB_ID() 
                    GROUP BY database_id
                '''
        cursor = server.New().cursor
        cursor.execute(query)
        return cursor.fetchone()[0]

    def print(self):
        print('\n-- Database Growth Projection --')
        print('Database size: {} MB'.format(self.database_size))
        print('Avg. Growth per 1000 insertions: {} MB'.format(str(self.growth)))
        print('Avg. Insertions per day: {}'.format(self.per_day))
        print('Avg. Growth per day: {} MB'.format(str(self.growth_per_day)))
        print('Avg. Growth per month: {} MB'.format(str(self.growth_per_month)))
        print('Months untill disk is full: {}\n'.format(self.months_untill_full))
