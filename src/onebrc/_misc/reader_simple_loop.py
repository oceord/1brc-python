import sys
from pathlib import Path

from onebrc.decorators.timeit import timeit


def _main(path):
    with path.open() as file:
        for _ in file:
            pass


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
