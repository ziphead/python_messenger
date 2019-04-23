
from cryptography.fernet import Fernet
from settings import KEY
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken
F_KEY = Fernet(KEY)


def encryption(message):
    try:
        data = F_KEY.encrypt(message)
        return data
    except (TypeError, AttributeError):
        return False


def decryption(message):
    try:
        data = F_KEY.decrypt(message)
        return data
    except (InvalidToken, InvalidSignature, NameError, TypeError):
        return False
