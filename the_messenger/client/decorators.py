import zlib
import inspect
import logging
from functools import wraps
from utilities import encryption, decryption
from settings import ENCRYPTION_STRICT

logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        info = inspect.stack()[0]
        logger.debug(f'{ info.function } - { request }')
        return func(request, *args, **kwargs)

    return wrapper


def compressed(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request:
            b_request = zlib.decompress(request)
            s_response = func(b_request, *args, **kwargs)
            return zlib.compress(s_response)
        else:
            return func(request, *args, **kwargs)

    return wrapper


def e_wrap(encoding_direction):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            info = inspect.stack()[0]
            if request:
                if encoding_direction == 'de' and ENCRYPTION_STRICT:
                    b_request = decryption(request)
                    if b_request:
                        logger.debug(
                            f'{ info.function } - sucsessful decryption')
                        s_response = func(b_request, *args, **kwargs)
                        return s_response
                    else:
                        logger.error(
                            f'{ info.function } - unsucsessful decryption  {request}')

                elif encoding_direction == 'en' and ENCRYPTION_STRICT:
                    b_request = encryption(request)
                    if b_request:
                        logger.debug(
                            f'{ info.function } - sucsessful encryption')
                        s_response = func(b_request, *args, **kwargs)
                        return s_response
                    else:
                        logger.error(
                            f'{ info.function } - unsucsessful encryption  {request}')
                else:
                    if request:
                        logger.debug(f'{ info.function } - NO encryption')
                        s_response = func(b_request, *args, **kwargs)
                        return s_response

            else:
                logger.error(f'request error - { request }')
                return func(request, *args, **kwargs)
        return wrapper
    return decorator
