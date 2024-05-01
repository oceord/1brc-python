import sys
from pathlib import Path

import dask.dataframe as dd

from onebrc.decorators.timeit import timeit, timeit_avg


def _main(path):
    res = (
        dd.read_csv(
            path,
            sep=";",
            header=None,
            names=["0", "1"],
            dtype={"0": str, "1": float},
        )
        .groupby("0")
        .agg(["min", "mean", "max"])
        .round({("1", "mean"): 1})
        .astype(str)
        .apply(
            lambda row: f"{row.name}=" + "/".join(v for v in row.to_numpy()),
            axis=1,
            meta=(None, "object"),
            result_type="reduce",
        )
        .compute()
        .to_list()
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
