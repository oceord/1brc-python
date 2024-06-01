import duckdb

from onebrc.decorators.timeit import exec_func, timeit


def _main(path):
    with duckdb.connect(database=path, read_only=True) as duckdb_conn:
        res = (
            duckdb.table("measurements", connection=duckdb_conn)
            .aggregate(
                group_expr="station",
                aggr_expr="station || '=' "
                "|| min(measurement) || '/' "
                "|| round(avg(measurement), 1) || '/' "
                "|| max(measurement) res",
            )
            .fetchall()
        )
        # print(*(row[0] for row in res), sep=", ")


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
