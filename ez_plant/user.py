from ez_plant.mongo_handler import MongoHandler

class User(object):
    def __init__(self, email, password, first_name="Anat", last_name="Eliyahu"):#TODO: default values are for debugging
        #self.id = Generator.generate_id() #need to find a module to do this
        self.username = email
        self.email = email
        self.password = password #TODO Roei will take care of encryption
        self.first_name = first_name
        self.last_name = last_name
        self.plants = []

    def save_to_database(self):
        mongo_worker = MongoHandler()
        mongo_worker.insert_object(vars(self), 'users')
