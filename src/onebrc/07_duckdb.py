import duckdb

from onebrc.decorators.timeit import timeit


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
