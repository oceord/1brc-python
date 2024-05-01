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
            pl.min("column_2").alias("min"),
            pl.mean("column_2").alias("mean"),
            pl.max("column_2").alias("max"),
        )
        .select(
            pl.col("column_1")
            + "="
            + pl.col("min").round(1).cast(pl.String)
            + "/"
            + pl.col("mean").round(1).cast(pl.String)
            + "/"
            + pl.col("max").round(1).cast(pl.String),
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
