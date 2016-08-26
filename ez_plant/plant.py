from ez_plant.mongo_handler import MongoHandler
from enum import Enum
import random
import string

class WaterMode(Enum):
    SCHEDULE = "schedule"
    MOISTURE = "moisture"

class Plant(object):
    def __init__(self, moisture_sensor_port, water_pump_port, plant_type, plant_id=None, name=None, water_data=None, image_url=None):
        if not plant_id:
            plant_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(12))

        self.plant_id = plant_id
        self.plant_type = plant_type
        self.name = name
        self.water_data = self.WateringData(water_data)
        self.image_url = image_url
        self.moisture_sensor_port = moisture_sensor_port
        self.water_pump_port = water_pump_port

    class WateringData(object):
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
        self.remove_from_database(username)
        mongo_worker.add_doc_to_array('users', { "username": username}, 'plants', self.to_doc())

    def remove_from_database(self, username):
        mongo_worker = MongoHandler()
        mongo_worker.delete_doc_from_array('users', { "username": username}, 'plants', { "plant_id": self.plant_id } )

    def update(self, username, m_port, w_port, plant_type, plant_name, water_data, image_url):
        self.moisture_sensor_port = m_port
        self.water_pump_port = w_port
        self.name = plant_name
        self.water_data = water_data
        self.image_url = image_url
        self.plant_type = plant_type

        mongo_worker = MongoHandler()
        mongo_worker.update_array_doc('users', { "username": username, "plants.plant_id": self.plant_id } , 'plants', self.to_doc())

    def to_doc(self):
        plant_doc = vars(self)
        return plant_doc
