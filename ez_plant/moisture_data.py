from ez_plant.mongo_handler import MongoHandler
import datetime

ARDUINO_MOISTURE_MIN_VALUE = 1024
MAX_PERCENTAGE = 100

class MoistureData(object):
    def __init__(self, username, plant_id, moisture, timestamp=None):
        self.username = username
        self.moisture = self.moisture_value_to_percentage(moisture)
        self.plant_id = plant_id
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.utcnow()

    def save_to_database(self):
        mongo_worker = MongoHandler()
        moisture_stats_object = {}
        moisture_stats_object['moisture'] = self.moisture
        moisture_stats_object['timestamp'] = self.timestamp
        mongo_worker.add_doc_to_nested_array('moisture_stats',
                                            { "username": self.username, "plants.plant_id": self.plant_id },
                                            'plants', 'stats', moisture_stats_object)

    def moisture_value_to_percentage(self, moisture):
        return float((abs(float(moisture) - ARDUINO_MOISTURE_MIN_VALUE) / ARDUINO_MOISTURE_MIN_VALUE) * 100)

    @staticmethod
    def percentage_to_moisture_value(percentage):
        return int(((MAX_PERCENTAGE - percentage) * ARDUINO_MOISTURE_MIN_VALUE) / MAX_PERCENTAGE)
