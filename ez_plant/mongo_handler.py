from pymongo import MongoClient
import datetime

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
        self.db[collection_name].insert_one(object)

    def get_single_object(self, collection_name, query):
        document = self.db[collection_name].find_one(query)
        return document

    def add_doc_to_array(self, collection_name, query, array_name, doc):
        self.db[collection_name].update_one(query, {'$push': {array_name: doc}})

    def delete_doc_from_array(self, collection_name, query, array_name, del_query):
        self.db[collection_name].update_one(query, {'$pull': {array_name: del_query}})

    def update_array_doc(self, collection_name, query, array_name, doc):
        array_with_dollar = '%s.$' % (array_name)
        self.db[collection_name].update_one(query, {'$set': {array_with_dollar: doc}})

    def add_doc_to_nested_array(self, collection_name, query, array_name, nested_array_name, doc):
        nested_array = '%s.$.%s' % (array_name, nested_array_name)
        self.db[collection_name].update(query, {'$push': {nested_array: doc}})

    def stats_aggregate(self, collection_name, username, plant_id):
        pipeline = [
            { "$match": { "username": username}},
            { "$unwind": "$plants"},
            { "$match": { "plants.plant_id": plant_id}},
            { "$unwind": "$plants.stats"},
            { "$match": { "plants.stats.timestamp": {"$gt": datetime.datetime.utcnow() - datetime.timedelta(1)}}},
            { "$project": { "plants.stats.timestamp":1, "plants.stats.moisture":1, "_id":0 }}
        ]

        res = list(self.db[collection_name].aggregate(pipeline))
        return res
