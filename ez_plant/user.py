from ez_plant.mongo_handler import MongoHandler
from flask.ext.login import UserMixin

class User(UserMixin):
    def __init__(self, email, password, first_name, last_name):
        self.username = email
        self.first_name = first_name
        self.last_name = last_name
        self.plants = []
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
