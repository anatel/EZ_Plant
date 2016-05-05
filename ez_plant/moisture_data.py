from ez_plant.mongo_handler import MongoHandler
import datetime

class MoistureData(object):
    def __init__(self, plant_id, moisture_value):
        self.plant_id = plant_id
        self.moisture_value = moisture_value
        self.timestamp = datetime.datetime.now()

    def save_to_database(self):
        mongo_worker = MongoHandler()
        mongo_worker.insert_object(vars(self), 'moisture_stats')
