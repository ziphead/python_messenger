import json
import socket
from datetime import datetime
from yaml import load, Loader
from argparse import ArgumentParser
from crypt.controller import decryption, encryption

from settings import (
    ENCODING_NAME, VARIABLE, HOST,
    PORT, BUFFERSIZE
)


host = HOST
port = PORT
encoding_name = ENCODING_NAME
buffersize = BUFFERSIZE

parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration'
)
args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        config = load(file, Loader=Loader)
        host = config.get('host') or HOST
        port = config.get('port') or PORT
        encoding_name = config.get('encoding_name') or ENCODING_NAME
        buffersize = config.get('buffersize') or BUFFERSIZE

try:
    sock = socket.socket()
    sock.connect((HOST, PORT))
    print(f'Client started with { HOST }:{ PORT }')

    action = input('Enter action to send:')
    data = input('Enter data to send:')

    request_string = json.dumps(
        {
            'action': action,
            'time': datetime.now().timestamp(),
            'data': data
        }
    )

    cypher_wrap = encryption(request_string.encode(ENCODING_NAME))
    sock.send(cypher_wrap)
    data = sock.recv(BUFFERSIZE)
    cypher_unwrap = decryption(data)
    print(cypher_unwrap.decode(ENCODING_NAME))
except KeyboardInterrupt:
    print('Client closed')
