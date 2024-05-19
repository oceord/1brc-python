import pyarrow as pa
import pyarrow.compute as pc
from pyarrow import csv

from onebrc.decorators.timeit import exec_func, timeit


def _main(path):
    agg_table = (
        csv.read_csv(
            path,
            read_options=csv.ReadOptions(column_names=["station", "temperature"]),
            parse_options=csv.ParseOptions(delimiter=";"),
            convert_options=csv.ConvertOptions(
                column_types={"station": pa.string(), "temperature": pa.float32()},
            ),
        )
        .group_by("station")
        .aggregate(
            [
                ("temperature", "min"),
                ("temperature", "mean"),
                ("temperature", "max"),
            ],
        )
    )
    # NOTE: could not find a performant way to separate station and values with '='
    res = pc.binary_join_element_wise(
        agg_table["station"],
        pc.cast(agg_table["temperature_min"], pa.string()),
        pc.cast(pc.round(agg_table["temperature_mean"], 1), pa.string()),
        pc.cast(agg_table["temperature_max"], pa.string()),
        "/",
    ).to_pylist()
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

    main(args.path, args.avg, args.timeout)
