from ez_plant.mongo_handler import MongoHandler
from enum import Enum
import random
import string
import datetime

class WaterMode(Enum):
    SCHEDULE = "schedule"
    MOISTURE = "moisture"


class Plant(object):
    def __init__(self, moisture_sensor_port, water_pump_port, plant_type,
                 plant_id=None, name=None, water_data=None, image_dir=None,
                 image_type=None, image_url=None, water_now=False):
        if not plant_id:
            plant_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(12))

        self.plant_id = plant_id
        self.plant_type = plant_type
        self.name = name
        self.water_data = self.WateringData(water_data)
        if image_url:
            self.image_url = image_url
        else:
            self.image_url = self.get_image_url(image_dir, image_type)
        self.moisture_sensor_port = moisture_sensor_port
        self.water_pump_port = water_pump_port
        self.water_now = water_now

    class WateringData(object):
        def __init__(self, water_data):
            if water_data:
                self.water_mode = water_data['water_mode']
                if self.water_mode == WaterMode.MOISTURE.value:
                    self.low_threshold = water_data['low_threshold']
                elif self.water_mode == WaterMode.SCHEDULE.value:
                    self.repeat_every = water_data['repeat_every']
                    self.hour = '%s:%s' % (water_data['hour'].split(':')[0].zfill(2), water_data['hour'].split(':')[1].zfill(2))
                    if 'next_watering' in water_data:
                        self.next_watering = water_data['next_watering']
                    else:
                        self.next_watering = self.calc_next_watering(self.repeat_every, self.hour)
                else:
                    raise ValueError

                if 'last_watered' in water_data:
                    self.last_watered = water_data['last_watered']
                else:
                    self.last_watered = None


        def calc_next_watering(self, repeat_every, hour):
            now = datetime.datetime.utcnow()
            dt_hour = datetime.datetime.strptime(hour, '%H:%M').time()
            time_now = now.time()
            if dt_hour >= time_now:
                next_watering = datetime.datetime.combine(now.date(), dt_hour)
            else:
                next_watering = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), dt_hour)

            return next_watering

    def save_to_database(self, username):
        mongo_worker = MongoHandler()
        self.remove_from_database(username)
        mongo_worker.add_doc_to_array('users', {"username": username}, 'plants', self.to_doc())

        moisture_stats_object = {}
        moisture_stats_object['plant_id'] = self.plant_id
        moisture_stats_object['stats'] = []
        mongo_worker.add_doc_to_array('moisture_stats', {"username": username}, 'plants', moisture_stats_object)

    def remove_from_database(self, username):
        mongo_worker = MongoHandler()
        mongo_worker.delete_doc_from_array('users', {"username": username}, 'plants', {"plant_id": self.plant_id})

    def remove_plant_stats(self, username):
        mongo_worker = MongoHandler()
        mongo_worker.delete_doc_from_array('moisture_stats', {"username": username}, 'plants', {"plant_id": self.plant_id})

    def update(self, username, m_port, w_port, plant_type, plant_name, water_data, image_dir, image_type):
        self.moisture_sensor_port = m_port
        self.water_pump_port = w_port
        self.name = plant_name
        print(self.water_data.last_watered)
        water_data['last_watered'] = self.water_data.last_watered
        self.water_data = self.WateringData(water_data)

        if image_dir and image_type:
            self.image_url = self.get_image_url(image_dir, image_type)
        self.plant_type = plant_type

        mongo_worker = MongoHandler()
        self.remove_from_database(username)
        mongo_worker.add_doc_to_array('users', {"username": username}, 'plants', self.to_doc())

    def get_image_url(self, image_dir, image_type):
        if hasattr(self, 'image_url'):
            curr_version = 0 if self.image_url is None else int(self.image_url.rsplit('-', 1)[1].split('.')[0]) + 1
        else:
            curr_version = 0

        if image_dir:
            return '%s/%s-%d.%s' % (image_dir, self.plant_id, curr_version, image_type)

        return None

    def get_stats(self, username):
        mongo_worker = MongoHandler()
        query_results = mongo_worker.stats_aggregate('moisture_stats', username, self.plant_id)
        return query_results

    def set_water_now(self, username):
        self.water_now = not self.water_now

        mongo_worker = MongoHandler()
        mongo_worker.update_array_doc('users', {"username": username, "plants.plant_id": self.plant_id}, 'plants', self.to_doc())

    def report_watering(self, username):
        self.water_now = False
        self.water_data.last_watered = datetime.datetime.utcnow()

        mongo_worker = MongoHandler()
        mongo_worker.update_array_doc('users', {"username": username, "plants.plant_id": self.plant_id}, 'plants', self.to_doc())

    def to_doc(self):
        plant_doc = vars(self)
        plant_doc['water_data'] = vars(self.water_data)
        return plant_doc
