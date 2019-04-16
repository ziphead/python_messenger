from .controller import (
    encryption,
    decryption,
)

routes = [
    {'action': 'encrypt', 'controller': encryption},
    {'action': 'decrypt', 'controller': decryption},
]
