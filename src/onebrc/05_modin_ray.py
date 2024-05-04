import modin.pandas as pd
import numpy as np

from onebrc.decorators.timeit import timeit


def _main(path):
    res = (
        pd.read_csv(
            path,
            sep=";",
            header=None,
            dtype={0: np.str_, 1: np.float32},
        )
        .groupby(0)
        .agg(["min", "mean", "max"])
        .round({(1, "mean"): 1})
        .astype(np.str_)
        .apply(
            lambda row: f"{row.name}=" + "/".join((v) for v in row.to_numpy()),
            axis=1,
            result_type="reduce",
        )
        .to_numpy()
        .tolist()
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
