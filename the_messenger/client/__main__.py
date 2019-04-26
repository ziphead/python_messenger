import json
import zlib
import socket
import logging
from datetime import datetime
from yaml import load, Loader
from argparse import ArgumentParser
from decorators import e_wrap


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

handler = logging.FileHandler('main.log', encoding=ENCODING_NAME)
error_handler = logging.FileHandler('error.log', encoding=ENCODING_NAME)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        handler,
        error_handler,
        logging.StreamHandler(),
    ]
)

@e_wrap('en')
def wrap_handler(json_data):   
    json_bytes = json_data.encode(ENCODING_NAME)
    json_bytes = zlib.compress(json_bytes)
    return json_bytes


@e_wrap('de')
def unwrap_handler(json_bytes):
    json_data= zlib.decompress(json_bytes)
    json_data = json_data.decode(ENCODING_NAME)
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
    # cypher_unwrap = unwrap_handler(data)
    # print(cypher_unwrap)
except KeyboardInterrupt:
    print('Client closed')
