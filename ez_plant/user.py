from ez_plant.mongo_handler import MongoHandler
from ez_plant.plant import Plant
from flask.ext.login import UserMixin

class User(UserMixin):
    def __init__(self, email, password, first_name, last_name, plants=None):
        self.username = email
        self.first_name = first_name
        self.last_name = last_name
        self.plants = []
        if plants:
            for plant in plants:
                self.plants.append(Plant(plant['id'], plant['name'], plant['water_data']))
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

    def add_plant(self, plant_id, plant_name, water_data):
        plant = Plant(plant_id, plant_name, water_data)
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
