import zlib
import inspect
import logging
from functools import wraps
from utilities import encryption, decryption
from protocol import make_403

logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        info = inspect.stack()[0]
        logger.debug(f'{ info.function } - { request }')
        return func(request, *args, **kwargs)

    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.get('user')
        if user:
            return func(request, *args, **kwargs)

        return make_403(request)

    return wrapper


def compressed(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        print('2 wrap', request)
        if request:
            b_request = zlib.decompress(request)
            s_response = func(b_request, *args, **kwargs)
            return zlib.compress(s_response)
        else:
            return func(request, *args, **kwargs)

    return wrapper


def e_wrap(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        print('1 wrap', request)
        if request:
            b_request = decryption(request)
            s_response = func(b_request, *args, **kwargs)
            return encryption(s_response)
        else:
            logger.error(f'encoding error - { request }')
            return func(request, *args, **kwargs)
    return wrapper
