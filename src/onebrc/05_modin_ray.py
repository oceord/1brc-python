import sys
from pathlib import Path

import modin.pandas as pd

from onebrc.decorators.timeit import timeit, timeit_avg


def _main(path):
    res = (
        pd.read_csv(
            path,
            sep=";",
            header=None,
            dtype={0: str, 1: float},
        )
        .groupby(0)
        .agg(["min", "mean", "max"])
        .apply(
            lambda row: f"{row.name}="
            + "/".join(str(round(v, 1)) for v in row.to_numpy()),
            axis=1,
            result_type="reduce",
        )
        .to_numpy()
        .tolist()
    )
    # print(*res, sep=", ")


@timeit
def main(path):
    _main(path)


@timeit_avg
def main_10(path):
    _main(path)


if __name__ == "__main__":
    _main(Path(sys.argv[1]))
    if "--avg" in sys.argv:
        main_10(Path(sys.argv[1]))
    else:
        main(Path(sys.argv[1]))
