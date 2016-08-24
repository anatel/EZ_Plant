from ez_plant.mongo_handler import MongoHandler
from ez_plant.plant import Plant
from flask.ext.login import UserMixin

AVAILABLE_MOISTURE_PORTS = [ 'A0', 'A1', 'A2', 'A3', 'A4', 'A5' ]
AVAILABLE_WATER_PUMP_PORTS = [ 2, 3, 4, 5, 6, 7 ]

class User(UserMixin):
    def __init__(self, email, password, first_name, last_name, plants=None):
        self.username = email
        self.first_name = first_name
        self.last_name = last_name
        self.plants = []
        if plants:
            for plant in plants:
                self.plants.append(Plant(plant['moisture_sensor_port'], plant['water_pump_port'], plant['id'], plant['name'], plant['water_data']))
        self.password = password

    def save_to_database(self):
        mongo_worker = MongoHandler()
        mongo_worker.insert_object(vars(self), 'users')

    @classmethod
    def get_from_database(self, username):
        mongo_worker = MongoHandler()
        user_doc = mongo_worker.get_single_object('users', { "username": username })
        return user_doc

    # override
    def get_id(self):
        return self.username

    def add_plant(self, m_port, w_port, plant_name, water_data, image_url):
        plant = Plant(m_port, w_port, name=plant_name, water_data=water_data, image_url=image_url)
        self.plants.append(plant)
        plant.save_to_database(self.username)

    def get_plant(self, plant_id):
        for plant in self.plants:
            if plant.id == plant_id:
                return plant

        return None

    def delete_plant(self, plant_id):
        for plant in self.plants:
            if plant.id == plant_id:
                plant_to_delete = plant

        if not plant_to_delete:
            raise ValueError

        self.plants.remove(plant_to_delete)
        plant_to_delete.remove_from_database(self.username)
        return True

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
