if __name__ == "__main__":
    import sys
    from pathlib import Path

    import polars as pl

    measurements_file = Path(sys.argv[1])
    output_parquet = f"{measurements_file!s}.{{INFO}}.parquet"

    input_df = pl.scan_csv(
        measurements_file,
        separator=";",
        has_header=False,
        schema={"station": pl.String, "measurement": pl.Float32},
    )
    input_df.sink_parquet(
        output_parquet.format(INFO="uncompressed"),
        compression="uncompressed",
    )
    input_df.sink_parquet(
        output_parquet.format(INFO="lz4"),
        compression="lz4",
    )
