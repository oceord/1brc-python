import sys
from collections import defaultdict
from csv import DictReader
from pathlib import Path

from onebrc.measure.timeit import timeit


@timeit
def main(path):
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
            ] or (
                0,
                0,
                0,
                0,
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
    print(
        *[
            f"{station}={min_}/{round(acc/count, 1)}/{max_}"
            for station, (min_, acc, max_, count) in acc.items()
        ],
        sep=", ",
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]))
