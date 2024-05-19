import inspect
import signal
import time
from math import ceil
from statistics import mean, variance

TIMEOUT = 120


def exec_func(func, timeout=TIMEOUT, *args, **kwargs):
    signal.signal(signal.SIGALRM, _signal_handler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        exec_time = end_time - start_time
    except TimeoutError:
        result = None
        exec_time = None
    finally:
        signal.alarm(0)

    return (result, exec_time)


def timeit(number_of_execs, timeout=TIMEOUT):
    def decorator(func):
        def wrapper(*args, **kwargs):
            exec_times = []
            func_module = ".".join(inspect.getmodule(func).__file__.split("/")[-2:])[
                :-3
            ]
            for _ in range(number_of_execs):
                result, exec_time = exec_func(func, timeout, *args, **kwargs)
                exec_times.append(exec_time)
            avg_exec_time = dceil(mean(exec_times), 3) if all(exec_times) else None
            exec_time_variance = (
                variance(exec_times)
                if len(exec_times) > 1 and all(exec_times)
                else None
            )
            print("Module:")
            print(f"    {func_module}")
            print("AvgExecTime / Variance:")
            print(f"    {avg_exec_time} / {exec_time_variance}")
            print("ExecTimes:")
            print(
                "    "
                + "\n    ".join(
                    f"({i}) {t}"
                    for i, t in sorted(
                        enumerate(exec_times),
                        key=lambda x: x[1] if x[1] is not None else -1,
                    )
                )
                + "\n",
            )
            return result

        return wrapper

    return decorator


def dceil(number, ndigits):
    multiplier = 10**ndigits
    return ceil(number * multiplier) / multiplier


def _signal_handler(_, __):
    raise TimeoutError
