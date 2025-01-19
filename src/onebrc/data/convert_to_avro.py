if __name__ == "__main__":
    import sys
    from pathlib import Path

    import fastavro
    import polars as pl

    measurements_file = Path(sys.argv[1])

    output_avro_parent = measurements_file.parent / measurements_file.stem
    avro_filename = f"{measurements_file.stem}.uncompressed.avro"
    output_avro_file = output_avro_parent / avro_filename

    output_avro_parent.mkdir(parents=True, exist_ok=True)

    if output_avro_file.exists():
        output_avro_file.unlink()

    schema = {
        "type": "record",
        "name": "Measurement",
        "fields": [
            {"name": "station", "type": "string"},
            {"name": "measurement", "type": "float"},
        ],
    }

    input_batched_reader = pl.read_csv_batched(
        measurements_file,
        separator=";",
        has_header=False,
        schema_overrides={"station": pl.String, "measurement": pl.Float32},
        batch_size=1_000_000,
    )

    with output_avro_file.open("wb") as avro_file:
        fastavro.writer(avro_file, schema, [])

    BATCH_VOL = 1
    batches = input_batched_reader.next_batches(BATCH_VOL)

    while batches:
        df_current_batches = pl.concat(batches)
        records = df_current_batches.to_dicts()

        with output_avro_file.open("a+b") as avro_file:
            fastavro.writer(avro_file, schema, records)

        batches = input_batched_reader.next_batches(BATCH_VOL)
