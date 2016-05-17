import uuid
from ez_plant.mongo_handler import MongoHandler
from ez_plant.hashing_handler import HashingHandler

class User(object):
    def __init__(self, email, password, first_name="Anat", last_name="Eliyahu"):
        self.user_id = uuid.uuid4().hex
        self.username = email
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.plants = []
        self.password = ""
        self._encrypt_password(password)

    def _encrypt_password(self, password):
        hashing_handler = HashingHandler()
        self.password = hashing_handler.encrypt(password)

    def save_to_database(self):
        mongo_worker = MongoHandler()
        mongo_worker.insert_object(vars(self), 'users')
