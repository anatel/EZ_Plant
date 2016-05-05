from passlib.hash import pbkdf2_sha256

class HashingHandler(object):
    def __init__(self):
        self.rounds = 200000
        self.salt_size = 16

    def encrypt(self, plain_text_string):
        encrypted_string = pbkdf2_sha256.encrypt(plain_text_string, rounds=self.rounds, salt_size=self.salt_size)
        return encrypted_string

    def verify(self, plain_text_string, encrypted_string):
        return pbkdf2_sha256.verify(plain_text_password, encrypted_password)
