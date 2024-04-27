import sys
from collections import defaultdict
from csv import DictReader
from pathlib import Path

from onebrc.decorators.timeit import timeit, timeit_avg


def _main(path):
    with path.open() as file:
        measurements = DictReader(
            file,
            delimiter=";",
            fieldnames=["station", "temperature"],
        )
        acc = defaultdict(tuple)
        for measurement in measurements:
            measurement_station = measurement["station"]
            measurement_temperature = float(measurement["temperature"])
            min_station, acc_station, max_station, count_station = acc[
                measurement_station
            ] or (0, 0, 0, 0)
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


@timeit
def main(path):
    _main(path)


@timeit_avg
def main_10(path):
    _main(path)


if __name__ == "__main__":
    if "--avg" in sys.argv:
        main_10(Path(sys.argv[1]))
    else:
        main(Path(sys.argv[1]))
