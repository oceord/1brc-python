import dask.dataframe as dd

from onebrc.decorators.timeit import exec_func, timeit


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
