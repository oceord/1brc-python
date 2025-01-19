if __name__ == "__main__":
    import shutil
    import sys
    from pathlib import Path

    import polars as pl

    measurements_file = Path(sys.argv[1])
    output_parquet_parent = (
        measurements_file.parent / measurements_file.stem / "parquet"
    )
    parquet_filename = "n{INDEX}.{INFO}.parquet"

    if output_parquet_parent.exists():
        shutil.rmtree(output_parquet_parent)
    output_parquet_parent.mkdir(parents=True, exist_ok=True)

    input_batched_reader = pl.read_csv_batched(
        measurements_file,
        separator=";",
        has_header=False,
        dtypes={"station": pl.String, "measurement": pl.Float32},
        batch_size=100_000,
    )
    batches = input_batched_reader.next_batches(100)
    i = 0
    while batches:
        df_current_batches = pl.concat(batches)
        df_current_batches.write_parquet(
            output_parquet_parent
            / parquet_filename.format(INDEX=f"{i:05d}", INFO="uncompressed"),
            compression="uncompressed",
        )
        i += 1
        batches = input_batched_reader.next_batches(100)
