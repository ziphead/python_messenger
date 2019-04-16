from cryptography.fernet import Fernet
from crypt.settings import KEY
from crypt.controller import encryption, decryption

DATA = 'Some data'
BYTES = b'gAAAAABctZhB2GK93qoQymFSNPqC_c8sSZEDtvvX7hBn3_NLiW7BcO4CT2dfhdhPoZYLb7jODW3FMrKyYaR4oYL-EU8UQqn7tg=='


def test_encryption():
    a = encryption(DATA)
    b = decryption(a)
    assert b == DATA


def test_decryption():
    b = decryption(BYTES)
    assert b == DATA
