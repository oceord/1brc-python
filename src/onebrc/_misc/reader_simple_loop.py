import sys
from pathlib import Path

from onebrc.measure.timeit import timeit, timeit_avg


def _main(path):
    with path.open() as file:
        for _ in file:
            pass


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
