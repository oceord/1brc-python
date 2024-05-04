if __name__ == "__main__":
    import sys
    from pathlib import Path

    import pandas as pd

    measurements_file = Path(sys.argv[1])

    measurements_df = pd.read_csv(
        measurements_file,
        sep=";",
        header=None,
        dtype={0: str, 1: float},
    )
    measurements_df[0] = pd.factorize(measurements_df[0])[0]
    measurements_df.to_csv(
        measurements_file.parent
        / (measurements_file.stem + "_int." + measurements_file.name.split(".")[-1]),
        sep=";",
        index=False,
        header=False,
    )
