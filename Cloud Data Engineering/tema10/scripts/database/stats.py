class Growth():

    def __init__(self):
        pass

    def projection(self, database, per_day: int, disk_size: int) -> dict:
        stats = database.command('dbstats')

        data_size = stats.get('dataSize')
        average_object_size = stats.get('avgObjSize')

        average_growth_per_day = average_object_size * per_day
        average_growth_per_month = average_growth_per_day * 30
        disk_size_in_bytes = disk_size * 1073741824

        months_until_full = (disk_size_in_bytes - data_size) / average_growth_per_month
        years_until_full = months_until_full / 12

        growth_projection = {"data_size": data_size,
                            "average_object_size": average_object_size,
                            "average_growth_per_day": average_growth_per_day,
                            "average_growth_per_month": average_growth_per_month,
                            "months_until_full": round(months_until_full, 0),
                            "years_until_full": round(years_until_full, 2)}
        
        print("\n***GROWTH PROJECTION***\n")
        print(f"Database size: {self.pretty_size(data_size, 'b')}")
        print(f"Average object size: {self.pretty_size(average_object_size, 'b')}")
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