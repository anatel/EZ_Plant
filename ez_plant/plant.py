from enum import Enum

class WaterMode(Enum):
    TIME = "schedule"
    MOISTURE = "moisture"

class Plant(object):
    def __init__(self, name, water_data):
        self.id = Generator.generate_id()
        self.name = name
        self.port_number = None #need to understand how arduino works
        self.water_data = self.WateringData(water_data)

    class WateringData(object): #add try catch
        def __init__(self, water_data):
            self.water_mode = water_data["water_mode"]
            if self.water_mode == WaterMode.MOISTURE.value:
                self.low = water_data["low_threshold"]
                #TODO add test if value is ok (if not empty of if exeed range)
                # self.high = water_data["high_threshold"]
            elif self.water_mode == WaterMode.TIME.value:
                # self.repeats = water_data["repeats"]
                self.repeat_every = water_data["repeat_every"]
                self.hour = water_data["hour"]
                # self.start_on = water_data["start_on"]
            else:
                return True
                #raise exception
            self.last_watered = None

    def save_to_database(self):
        mongo_worker = MongoHandler()
        mongo_worker.insert_object(vars(self), 'plants')

    @classmethod
    def get_from_database(self, plantid):
        mongo_worker = MongoHandler()
        plant_doc = mongo_worker.get_single_object('plants', { "id": plantid })
        return user_doc

    # override
    def get_id(self):
        return self.id
