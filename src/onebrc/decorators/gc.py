import gc


def no_gc(func):
    def wrapper(*args, **kwargs):
        gc.disable()
        result = func(*args, **kwargs)
        gc.enable()
        return result

    return wrapper
