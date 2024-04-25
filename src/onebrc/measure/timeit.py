import inspect
import time


def timeit(func):
    def wrapper(*args, **kwargs):
        func_module = ".".join(inspect.getmodule(func).__file__.split("/")[-2:])[:-3]
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"\n\t{func_module}.{func.__name__}\t=>\t{execution_time} seconds\n")
        return result

    return wrapper
