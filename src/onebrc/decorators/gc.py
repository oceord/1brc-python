import gc
from functools import wraps


def no_gc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        gc.disable()
        result = func(*args, **kwargs)
        gc.enable()
        return result

    return wrapper
