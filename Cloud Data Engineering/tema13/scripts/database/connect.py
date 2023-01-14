import pyodbc as redshift

class Redshift:

    def __init__(self) -> None:
        pass

    def connect(self) -> redshift.Connection:
        connection = redshift.connect('DSN=Redshift')
        return connection