from ez_plant.mongo_handler import MongoHandler
from enum import Enum

class WaterMode(Enum):
    SCHEDULE = "schedule"
    MOISTURE = "moisture"

class Plant(object):
    def __init__(self, plant_id=None, name=None, water_data=None):
        self.id = plant_id
        self.name = name
        self.port_number = None #need to understand how arduino works
        self.water_data = self.WateringData(water_data)

    class WateringData(object): #add try catch
        def __init__(self, water_data):
            if water_data:
                self.water_mode = water_data['water_mode']
                if self.water_mode == WaterMode.MOISTURE.value:
                    self.low_threshold = water_data['low_threshold'] #TODO add test if value is ok (if not empty of if exeed range)
                elif self.water_mode == WaterMode.SCHEDULE.value:
                    self.repeat_every = water_data['repeat_every']
                    self.hour = water_data['hour']
                else:
                    raise ValueError

                self.last_watered = None

    def save_to_database(self, username):
        mongo_worker = MongoHandler()
        plant_doc = vars(self)
        plant_doc['water_data'] = vars(self.water_data)
        mongo_worker.add_doc_to_array('users', { "username": username}, 'plants', plant_doc)

    def remove_from_database(self, username):
        mongo_worker = MongoHandler()
        mongo_worker.delete_doc_from_array('users', { "username": username}, 'plants', { "id": self.id } )
