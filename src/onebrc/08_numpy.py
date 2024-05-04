import numpy as np
import pandas as pd

from onebrc.decorators.timeit import timeit


def _main(path):
    # the fastest way to read CSV is to use pandas, np.genfromtxt is too slow
    data = pd.read_csv(
        path,
        sep=";",
        header=None,
        dtype={0: str, 1: float},
    ).to_numpy()
    unique_stations, station_indices = np.unique(
        data.transpose()[0],
        return_inverse=True,
    )
    res = []
    for station in unique_stations:
        station_data = data[
            station_indices == np.where(unique_stations == station)[0][0]
        ]
        station_temperatures = station_data.transpose()[1]
        res.append(
            f"{station!s}={np.min(station_temperatures)!s}/"
            f"{round(np.mean(station_temperatures), 1)!s}/"
            f"{np.max(station_temperatures)!s}",
        )
    # print(*res, sep=", ")


def main(path, number_of_execs, timeout):
    timeit(number_of_execs=number_of_execs, timeout=timeout)(_main)(path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--avg", type=int, required=True)
    parser.add_argument("-t", "--timeout", type=int, required=True)
    args = parser.parse_args()

    main(args.path, args.avg, args.timeout)
