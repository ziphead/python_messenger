import json
import socket
import logging

from yaml import load, Loader
from argparse import ArgumentParser
from crypt.controller import decryption, encryption

import settings

from routes import resolve
from protocol import (
    validate_request, make_response,
    make_400, make_404, wrong_encryption_response
)
from settings import (
    ENCODING_NAME, HOST,
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

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    logging.info(f'Server started with { host }:{ port }')
    while True:
        client, address = sock.accept()
        logging.info(f'Client detected { address }')
        b_request = client.recv(buffersize)
        if decryption(b_request):
            b_request = decryption(b_request)
            request = json.loads(
                b_request.decode(ENCODING_NAME)
            )

            action_name = request.get('action')

            if validate_request(request):
                controller = resolve(action_name)
                if controller:
                    try:
                        response = controller(request)

                        if response.get('code') != 200:
                            logging.error(f'Request is not valid')
                        else:
                            logging.info(
                                f'Function { controller.__name__ } was called')
                    except Exception as err:
                        logging.critical(err)
                        response = make_response(
                            request, 500, 'Internal server error'
                        )
                else:
                    logging.error(f'Action { action_name } does not exits')
                    response = make_404(request)
            else:
                logging.error(f'Request is not valid')
                response = make_400(request)

        else:
            logging.error(f'Security Failure')
            response = wrong_encryption_response(900,address)
        
        s_response = encryption(json.dumps(response).encode(ENCODING_NAME))
        client.send(s_response)

except KeyboardInterrupt:
    logging.info('Client closed')
