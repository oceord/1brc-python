from pathlib import Path

from onebrc.decorators.timeit import exec_func, timeit


def _main(path):
    with path.open() as file:
        acc = {}
        for line in file:
            measurement_station, str_temperature = line.split(";")
            measurement_temperature = float(str_temperature)
            min_station, acc_station, max_station, count_station = acc.get(
                measurement_station,
                (0, 0, 0, 0),
            )
            acc[measurement_station] = (
                (
                    measurement_temperature
                    if measurement_temperature < min_station
                    else min_station
                ),
                acc_station + measurement_temperature,
                (
                    measurement_temperature
                    if measurement_temperature > max_station
                    else max_station
                ),
                count_station + 1,
            )
    res = [
        f"{station}={min_}/{round(acc/count, 1)}/{max_}"
        for station, (min_, acc, max_, count) in acc.items()
    ]
    # print(*res, sep=", ")


def main(path, number_of_execs, timeout):
    exec_func(_main, timeout, path)
    timeit(number_of_execs=number_of_execs, timeout=timeout)(_main)(path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--avg", type=int, required=True)
    parser.add_argument("-t", "--timeout", type=int, required=True)
    args = parser.parse_args()

    main(Path(args.path), args.avg, args.timeout)
