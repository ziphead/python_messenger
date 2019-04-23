import json
import socket
from datetime import datetime
from yaml import load, Loader
from argparse import ArgumentParser
from decorators import compressed, e_wrap


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

@compressed
@e_wrap('en')
def wrap_handler(json_data):
    json_bytes = json_data.encode(ENCODING_NAME)
    return json_bytes


@e_wrap('de')
@compressed
def unwrap_handler(json_bytes):
    json_data = json_bytes.decode(ENCODING_NAME)
    return json_data


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

    cypher_wrap = wrap_handler(request_string)
    sock.send(cypher_wrap)
    data = sock.recv(BUFFERSIZE)
    cypher_unwrap = unwrap_handler(data)
    # print(cypher_unwrap.decode(ENCODING_NAME))
except KeyboardInterrupt:
    print('Client closed')
