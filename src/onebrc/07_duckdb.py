import sys
from pathlib import Path

import duckdb

from onebrc.decorators.timeit import timeit, timeit_avg


def _main(path):
    res = (
        duckdb.read_csv(
            path,
            sep=";",
            header=False,
            dtype=["varchar", "double"],
        )
        .aggregate(
            group_expr="column0",
            aggr_expr="column0 || '=' "
            "|| min(column1) || '/' "
            "|| round(avg(column1), 1) || '/' "
            "|| max(column1) res",
        )
        .fetchall()
    )
    # print(*(row[0] for row in res), sep=", ")


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
