import sys
from pathlib import Path

from onebrc.measure.timeit import timeit_avg


@timeit_avg
def main(path):
    with path.open() as file:
        for _ in file:
            pass


if __name__ == "__main__":
    main(Path(sys.argv[1]))
