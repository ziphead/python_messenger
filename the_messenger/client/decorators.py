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


def e_wrap(encoding_direction):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            info = inspect.stack()[0]
            if request:
                print(f'ecwrap {encoding_direction}', request)

                if encoding_direction == 'de' and ENCRYPTION_STRICT:
                    b_request = decryption(request)
                    print('b_request ', b_request)
                    func_job = func(b_request, *args, **kwargs)
                    if b_request:
                        logger.debug(
                            f'{ info.function } - sucsessful decryption')

                        return func_job
                    else:
                        logger.error(
                            f'{ info.function } - unsucsessful decryption  {request}')

                elif encoding_direction == 'en' and ENCRYPTION_STRICT:
                    func_job = func(request, *args, **kwargs)
                    b_request = encryption(func_job)
                    if b_request:
                        logger.debug(
                            f'{ info.function } - sucsessful encryption')
                        return b_request
                    else:
                        logger.error(
                            f'{ info.function } - unsucsessful encryption  {request}')
                else:

                    logger.debug(f'{ info.function } - NO encryption')
                    return func_job

            else:
                logger.error(f'request error - { request }')
                return func(request, *args, **kwargs)
        return wrapper
    return decorator
