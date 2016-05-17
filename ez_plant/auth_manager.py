from ez_plant.mongo_handler import MongoHandler
from ez_plant.hashing_handler import HashingHandler

class AuthManager(object):
    def __init__(self):
        pass

    def _get_user_db_object(self, username):
        mongo_worker = MongoHandler()
        user_doc = mongo_worker.get_single_object('users', { "user_id": self.user_id })
        return user_doc

    def check_if_user_exists(self, username):
        user_doc = self._get_user_db_object(username)
        if not user_doc:
            return False

        return True

    def verify_user_password(self, username, password):
        user_doc = self._get_user_db_object(username)
        hashing_handler = HashingHandler()
        
