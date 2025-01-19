import duckdb

from onebrc.decorators.timeit import exec_func, timeit


def _main(path):
    con = duckdb.connect()
    con.execute(
        """
        INSTALL avro FROM community;
        LOAD avro;""",
    )
    stmt = f"""
        SELECT
            station || '=' ||
            MIN(measurement) || '/' ||
            ROUND(AVG(measurement), 1) || '/' ||
            MAX(measurement) AS res
        FROM read_avro('{path}')
        GROUP BY station;
        """
    res = con.execute(stmt).fetchall()
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
