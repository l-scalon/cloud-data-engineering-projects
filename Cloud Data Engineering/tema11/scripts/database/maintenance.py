from database.execute import Query
from database.connect import MySQL as server
from database.variables import Variable as env
import os

class Maintenance:

    def __init__(self) -> None:
        pass

    def null_cleanup(self, connection):
        query = ('CALL contabyx.delete_null_from_transfers();')
        Query().execute(connection = connection, query = query)

    def reindex(self, connection):
        if not connection.is_connected(): server().reconnect()
        host = server().get_host()
        keypair_path = env().config_path
        keypair = os.path.join(keypair_path, env().get('KEYPAIR'))
        password = env().get('PASSWORD')
        os.system(f'ssh -i "{keypair}" ec2-user@{host} -o StrictHostKeyChecking=no "docker exec mysql /usr/bin/mysqlcheck -u root --password={password} --auto-repair --optimize contabyx"')
        os.system(f'ssh -i "{keypair}" ec2-user@{host} -o StrictHostKeyChecking=no "docker exec mysql /usr/bin/mysqlcheck -u root --password={password} --auto-repair --optimize information_schema"')

    def analyze(self, connection):
        query = ('call contabyx.analyze_all();')
        Query().execute(connection = connection, query = query)

    def default(self, connection):
        self.null_cleanup(connection)
        self.reindex(connection)
        self.analyze(connection)

class Growth:

    def __init__(self) -> None:
        pass

    def projection(self, connection, per_day: int, disk_size: int) -> dict:
        query = 'SELECT SUM(AVG_ROW_LENGTH) FROM information_schema.TABLES WHERE TABLE_SCHEMA = "contabyx"'
        average_row_size = Query().execute(connection = connection, query = query)[0][0]
        query = 'SELECT ROUND(SUM(data_length + index_length), 1) FROM information_schema.tables  WHERE table_schema = "contabyx" GROUP BY table_schema; '
        data_size = Query().execute(connection = connection, query = query)[0][0]

        average_growth_per_day = average_row_size * per_day
        average_growth_per_month = average_growth_per_day * 30
        disk_size_in_bytes = disk_size * 1073741824

        months_until_full = (disk_size_in_bytes - data_size) / average_growth_per_month
        years_until_full = months_until_full / 12

        growth_projection = {"data_size": data_size,
                            "average_object_size": average_row_size,
                            "average_growth_per_day": average_growth_per_day,
                            "average_growth_per_month": average_growth_per_month,
                            "months_until_full": round(months_until_full, 0),
                            "years_until_full": round(years_until_full, 2)}
        
        print("\n***GROWTH PROJECTION***\n")
        print(f"Database size: {self.pretty_size(data_size, 'b')}")
        print(f"Average object size: {self.pretty_size(average_row_size, 'b')}")
        print(f"Average growth per day: {self.pretty_size(average_growth_per_day, 'b')}")
        print(f"Average growth per month: {self.pretty_size(average_growth_per_month, 'b')}")
        print(f"Months until full: {round(months_until_full, 0)}")
        print(f"Years until full: {round(years_until_full, 0)}\n")

        return growth_projection

    def pretty_size(self, size, unity):
        unities = ['b', 'k', 'm', 'g']
        pretty_unities = ['bytes', 'KB', 'MB', 'GB']
        index = unities.index(unity)
        
        count = 0
        while size > 1024:
            size = self.convert(size)
            count += 1
        index = index + count

        return f'{round(size, 2)} {pretty_unities[index]}'

    def convert(self, size):
        return size / 1024