import inspect
import time
from math import ceil
from statistics import mean


def timeit(func):
    def wrapper(*args, **kwargs):
        func_module = ".".join(inspect.getmodule(func).__file__.split("/")[-2:])[:-3]
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = decimal_ceil(end_time - start_time, 3)  # seconds
        print("Module:")
        print(f"    {func_module}.{func.__name__}")
        print("ExecTime:")
        print(f"    {execution_time}" + "\n")
        return result

    return wrapper


def timeit_avg(func):
    def wrapper(*args, **kwargs):
        number_of_execs = 10
        exec_times = []
        func_module = ".".join(inspect.getmodule(func).__file__.split("/")[-2:])[:-3]
        for _ in range(number_of_execs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time  # seconds
            exec_times.append(execution_time)
        avg_execution_time = decimal_ceil(mean(exec_times), 3)
        print("Module:")
        print(f"    {func_module}.{func.__name__}")
        print("AvgExecTime:")
        print(f"    {avg_execution_time}")
        print("ExecTimes:")
        print(
            "    " + "\n    ".join(str(t) for t in sorted(exec_times)) + "\n",
        )
        return result

    return wrapper


def decimal_ceil(number, ndigits):
    multiplier = 10**ndigits
    return ceil(number * multiplier) / multiplier
