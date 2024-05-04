import polars as pl

from onebrc.decorators.timeit import exec_func, timeit


def _main(path):
    res = (
        pl.scan_csv(
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
        .collect(streaming=True)
        .to_series()
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
