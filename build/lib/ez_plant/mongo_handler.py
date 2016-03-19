from pymongo import MongoClient

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class MongoHandler(object):
    def __init__(self):
        self.database_name = 'ez_plant'
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[self.database_name]

    def insert_object(self, object, collection_name):
        insert_result = self.db[collection_name].insert_one(object)

    def delete_object(self):
        return True

    def get_object(self):
        return True
