from cryptography.fernet import Fernet
from crypt.settings import KEY

F_KEY = Fernet(KEY)


def encryption(message):
    data = message.encode('utf-8')
    data = F_KEY.encrypt(data)
    return data


def decryption(message):
    data = F_KEY.decrypt(message)
    data = data.decode('utf-8')
    return data
