from random import randint

class Datetime():

    def __init__(self):
        pass

    def random(self)->str:
        years = [2019, 2020, 2021, 2022]
        seed = randint(1, 42)
        floor = seed // 12
        year = years[floor]
        month = (seed % 12) + 1
        if month == 2: day = randint(1, 28)
        else: day = randint(1, 30)
        hour, minutes, seconds = randint(0, 23), randint(0, 59), randint(0, 59)
        return '{}-{}-{} {}:{}:{}.000'.format(year, month, day, hour, minutes, seconds)
