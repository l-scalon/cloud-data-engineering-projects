from bson import ObjectId
from database.connect import SQLServer as sql
from database.connect import MongoDB as mdb
from database.select import SQLServer as query

class Prepare():

    def __init__(self):
        pass
    
    def create_database(self):
        database_name = sql().database
        database = mdb().get_database(database_name)
        return database

    def create_collections(self, database, collections: list):
        for collection in collections:
            new_collection = database[collection]

    def create_ids(self, table: tuple) -> dict:
        table_ids = query().select(columns = table[1], table = table[0])
        index = []
        for id in table_ids:
            index.append(id[0])
        ids_to_objectIDs = self.index_into_objectID(index)
        return ids_to_objectIDs
    
    def index_into_objectID(self, index: list) -> dict:
        index_to_objectID_dict = {}
        for id in index:
            index_to_objectID_dict[id] = ObjectId()
        return index_to_objectID_dict