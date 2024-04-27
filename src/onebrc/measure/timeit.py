import inspect
import time
from statistics import mean


def timeit(func):
    def wrapper(*args, **kwargs):
        func_module = ".".join(inspect.getmodule(func).__file__.split("/")[-2:])[:-3]
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time # seconds
        print(f"\nModule:\t\t{func_module}.{func.__name__}")
        print(f"ExecTime:\t{execution_time}\n")
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
            execution_time = end_time - start_time # seconds
            exec_times.append(execution_time)
        avg_execution_time = mean(exec_times)
        print(f"\nModule:\t\t{func_module}.{func.__name__}")
        print(f"AvgExecTime:\t{avg_execution_time}")
        print(f"ExecTimes:\t{"\n\t\t\t".join(str(t) for t in sorted(exec_times))}\n")
        return result

    return wrapper