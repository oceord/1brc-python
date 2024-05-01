import sys
from pathlib import Path

import polars as pl

from onebrc.decorators.timeit import timeit, timeit_avg


def _main(path):
    res = (
        pl.read_csv(
            path,
            separator=";",
            has_header=False,
            schema={"column_1": pl.String, "column_2": pl.Float32},
        )
        .group_by("column_1")
        .agg(
            pl.col("column_2").min().alias("min"),
            pl.col("column_2").mean().alias("mean"),
            pl.col("column_2").max().alias("max"),
        )
        .map_rows(
            lambda row: f"{row[0]}=" + "/".join(str(round(v, 1)) for v in row[1:]),
        )
        .to_series()
    )
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
