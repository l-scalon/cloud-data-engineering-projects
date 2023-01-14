from math import isclose

class Compare:

    def __init__(self):
        pass

    def is_equal(self, source, target, database: str, tables: list):
        for table in tables:
            select = f'SELECT * FROM {database}.{table}'
            source.execute(select)
            target.execute(select)
            for result_source, result_target in zip(source.fetchall(), target.fetchall()):
                equals = True if all(source_data == target_data for source_data, target_data in zip(result_source, result_target)) else False
                if equals == False: equals = self.is_close(result_source, result_target)
            print(f'{table}: {equals}')

    def is_close(self, source, target):
        for source_data, target_data in zip(source, target):
            if not type(source_data) == type(target_data): return False
            elif not isinstance(source_data, float) and not source_data == target_data: return False
            elif not isclose(source_data, target_data, abs_tol = 0.1): return False
            else: return True