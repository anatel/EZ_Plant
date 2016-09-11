from ez_plant.mongo_handler import MongoHandler
from ez_plant.plant import Plant
from flask.ext.login import UserMixin

AVAILABLE_MOISTURE_PORTS = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']
AVAILABLE_WATER_PUMP_PORTS = [2, 3, 4, 5, 6]

class User(UserMixin):
    def __init__(self, email, password, first_name, last_name, plants=None):
        self.username = email
        self.first_name = first_name
        self.last_name = last_name
        self.plants = []
        if plants:
            for plant in plants:
                self.plants.append(Plant(plant['moisture_sensor_port'], plant['water_pump_port'],
                                         plant['plant_type'], plant['plant_id'],
                                         plant['name'], plant['water_data'], image_url=plant['image_url'],
                                         water_now=plant['water_now']))
        self.password = password

    def save_to_database(self):
        mongo_worker = MongoHandler()
        mongo_worker.insert_object(vars(self), 'users')
        moisture_stats_object = {}
        moisture_stats_object['plants'] = []
        moisture_stats_object['username'] = self.username
        mongo_worker.insert_object(moisture_stats_object, 'moisture_stats')

    @classmethod
    def get_from_database(self, username):
        mongo_worker = MongoHandler()
        user_doc = mongo_worker.get_single_object('users', {"username": username})
        return user_doc

    # override
    def get_id(self):
        return self.username

    def add_plant(self, m_port, w_port, plant_type, plant_name, water_data, image_dir, image_type):
        plant = Plant(m_port, w_port, plant_type, name=plant_name, water_data=water_data,
                      image_dir=image_dir, image_type=image_type)
        self.plants.append(plant)
        plant.save_to_database(self.username)

        return plant

    def update_plant(self, plant_id, m_port, w_port, plant_type, plant_name, water_data, image_dir, image_type):
        plant_to_update = self.get_plant(plant_id)
        plant_to_update.update(self.username, m_port, w_port, plant_type,
                               plant_name, water_data, image_dir=image_dir, image_type=image_type)

        return plant_to_update

    def get_plant(self, plant_id):
        for plant in self.plants:
            if plant.plant_id == plant_id:
                return plant

        return None

    def delete_plant(self, plant_id):
        plant_to_delete = self.get_plant(plant_id)
        if not plant_to_delete:
            raise ValueError

        self.plants.remove(plant_to_delete)
        plant_to_delete.remove_from_database(self.username)
        plant_to_delete.remove_plant_stats(self.username)

    def get_free_ports(self, port_type):
        used_ports = []
        if port_type != 'moisture' and port_type != 'water_pump':
            raise ValueError

        available_ports = AVAILABLE_MOISTURE_PORTS if port_type == 'moisture' else AVAILABLE_WATER_PUMP_PORTS
        port_field = 'moisture_sensor_port' if port_type == 'moisture' else 'water_pump_port'
        if self.plants:
            for plant in self.plants:
                used_ports.append(getattr(plant, port_field))

        free_ports = list(set(available_ports) - set(used_ports))
        free_ports.sort()
        return free_ports
