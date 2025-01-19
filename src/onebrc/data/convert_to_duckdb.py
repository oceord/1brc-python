import sys
from pathlib import Path

if __name__ == "__main__":
    import duckdb

    measurements_file = Path(sys.argv[1])
    output_db = f"{measurements_file!s}.duckdb"
    output_db_indexed = f"{measurements_file!s}.indexed.duckdb"

    if Path(output_db).exists():
        Path(output_db).unlink()

    with duckdb.connect(database=output_db, read_only=False) as duckdb_conn:
        duckdb_conn.execute(
            f"""
            CREATE TABLE measurements AS
            SELECT station, measurement
            FROM read_csv(
                '{measurements_file!s}',
                delim=';',
                header=false,
                columns={{'station': 'VARCHAR', 'measurement': 'DOUBLE'}}
            );""",  # noqa: S608
        )
