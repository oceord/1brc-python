# onebrc

![Python](https://img.shields.io/badge/python-006d98?style=for-the-badge&logo=python&logoColor=ffc600)
![Docker](https://img.shields.io/badge/docker-2496ed?style=for-the-badge&logo=docker&logoColor=ffffff)

This repository contains various approaches to solve [1️⃣🐝🏎️ The One Billion Row Challenge](https://github.com/gunnarmorling/onebrc) using the Python ecosystem.
Contrary to the rules of the challenge, external dependencies are used.

A roadmap is available [here](ROADMAP.md).

## Execution Benchmarks

Next, follow benchmarks for all solutions for 3 sample sizes: 100 million, 200 million, and 1 billion.
Only solutions that took less than 5 seconds for a sample size of 100 million were considered in samples bigger than that.
200 million is the largest sample size that allowed (almost) all solutions to run without being killed by the Out Of Memory Killer (OOM Killer), "a process that the linux kernel employs when the system is critically low on memory" [[source](https://neo4j.com/developer/kb/linux-out-of-memory-killer/)].
Solutions killed are marked with KILLED.
These benchmarks are the Average Execution Time (AET) in seconds for 10 executions.
The variance (VAR) is also presented alongside each individual benchmark.
Please refer to [exec_logs](./exec_logs/) for the full execution logs of these benchmarks.
A timeout of 2 minutes has been set for each individual execution.
Solutions that timed-out are identified with TIMEOUT.
Please refer to [Python Implementations](#python-implementations) for more information on the variants used.

### Sample Size: 100 million (1.5G)

| Solution                                                  | CPython AET/VAR | CPython_PerfOpt AET/VAR | CPython_PerfOpt NoGC AET/VAR |
| :-------------------------------------------------------- | --------------: | ----------------------: | ---------------------------: |
| `00_native_DictReader`                                    | 101.018 / 0.270 |          83.905 / 0.171 |                83.84 / 0.651 |
| `01_native_split`                                         |  39.651 / 0.091 |          34.303 / 0.122 |               35.148 / 0.702 |
| `02_native_read_text`                                     |  43.390 / 0.224 |          38.652 / 0.105 |               38.144 / 0.032 |
| `03_pandas`                                               |  23.727 / 0.034 |          21.028 / 0.009 |                           NA |
| `03_pandas_pyarrow`                                       |   8.706 / 0.005 |           8.199 / 0.004 |                           NA |
| `04_dask`                                                 |  17.312 / 0.009 |          16.642 / 0.009 |                           NA |
| `04_dask_pyarrow`                                         |   6.989 / 0.004 |           6.932 / 0.004 |                           NA |
| `05_modin_ray`                                            |  31.191 / 0.325 |          29.237 / 0.058 |                           NA |
| `06_polars_read_csv`                                      |   4.322 / 0.012 |           4.386 / 0.023 |                           NA |
| `06_polars_scan_csv`                                      |   4.545 / 0.006 |           4.639 / 0.019 |                           NA |
| `06_polars_scan_csv_streaming`                            |   2.454 / 0.000 |           2.457 / 0.000 |                           NA |
| `07_duckdb`                                               |   2.293 / 0.000 |           2.291 / 0.000 |                           NA |
| `07_duckdb_parallel`                                      |   2.683 / 0.022 |           2.674 / 0.022 |                           NA |
| `08_numpy`                                                |         TIMEOUT |                 TIMEOUT |                           NA |
| `09_pyarrow`                                              |   1.494 / 0.000 |           1.488 / 0.001 |                           NA |
| `10_parquet_polars_read_parquet` (uncompressed)           |   3.988 / 0.021 |           3.776 / 0.016 |                           NA |
| `10_parquet_polars_scan_parquet` (uncompressed)           |   4.107 / 0.024 |           3.848 / 0.012 |                           NA |
| `10_parquet_polars_scan_parquet_streaming` (uncompressed) |   2.045 / 0.000 |           2.049 / 0.000 |                           NA |
| `10_parquet_duckdb` (uncompressed)                        |   1.587 / 0.000 |           1.583 / 0.000 |                           NA |
| `10_parquet_pyarrow` (uncompressed)                       |   1.104 / 0.002 |           1.084 / 0.000 |                           NA |
| `10_parquet_pyarrow_memory_map` (uncompressed)            |   1.030 / 0.002 |           1.017 / 0.000 |                           NA |
| `10_parquet_polars_read_parquet` (lz4)                    |   4.164 / 0.009 |           4.004 / 0.013 |                           NA |
| `10_parquet_polars_scan_parquet` (lz4)                    |   4.162 / 0.013 |           3.911 / 0.027 |                           NA |
| `10_parquet_polars_scan_parquet_streaming` (lz4)          |   2.138 / 0.000 |           2.134 / 0.000 |                           NA |
| `10_parquet_duckdb` (lz4)                                 |   1.646 / 0.000 |           1.649 / 0.000 |                           NA |
| `10_parquet_pyarrow` (lz4)                                |   1.125 / 0.001 |           1.111 / 0.000 |                           NA |
| `10_parquet_pyarrow_memory_map` (lz4)                     |   1.053 / 0.000 |           1.050 / 0.000 |                           NA |
| `11_duckdb_duckdb`                                        |   1.120 / 0.000 |           1.143 / 0.000 |                           NA |

### Sample Size: 200 million (3.0G)

| Solution                                                  | CPython AET/VAR | CPython_PerfOpt AET/VAR |
| :-------------------------------------------------------- | --------------: | ----------------------: |
| `06_polars_read_csv`                                      |  10.383 / 0.325 |          11.147 / 0.151 |
| `06_polars_scan_csv`                                      |  10.521 / 0.022 |          10.969 / 0.066 |
| `06_polars_scan_csv_streaming`                            |   4.907 / 0.000 |           4.872 / 0.000 |
| `07_duckdb`                                               |   4.905 / 0.230 |           4.950 / 0.218 |
| `07_duckdb_parallel`                                      |   5.411 / 0.001 |           5.391 / 0.000 |
| `09_pyarrow`                                              |   3.115 / 0.050 |           3.104 / 0.041 |
| `10_parquet_polars_read_parquet` (uncompressed)           |          KILLED |                  KILLED |
| `10_parquet_polars_scan_parquet` (uncompressed)           |   9.379 / 0.199 |           9.579 / 0.107 |
| `10_parquet_polars_scan_parquet_streaming` (uncompressed) |   4.087 / 0.000 |           4.089 / 0.000 |
| `10_parquet_duckdb` (uncompressed)                        |   3.159 / 0.000 |           3.158 / 0.000 |
| `10_parquet_pyarrow` (uncompressed)                       |   2.266 / 0.005 |           2.268 / 0.005 |
| `10_parquet_pyarrow_memory_map` (uncompressed)            |   2.054 / 0.003 |           2.051 / 0.010 |
| `10_parquet_polars_read_parquet` (lz4)                    |          KILLED |                  KILLED |
| `10_parquet_polars_scan_parquet` (lz4)                    |   9.725 / 0.117 |           9.613 / 0.100 |
| `10_parquet_polars_scan_parquet_streaming` (lz4)          |   4.284 / 0.000 |           4.268 / 0.000 |
| `10_parquet_duckdb` (lz4)                                 |   3.298 / 0.000 |           3.294 / 0.000 |
| `10_parquet_pyarrow` (lz4)                                |   2.338 / 0.004 |           2.316 / 0.002 |
| `10_parquet_pyarrow_memory_map` (lz4)                     |   2.146 / 0.008 |           2.154 / 0.007 |
| `11_duckdb_duckdb`                                        |   2.209 / 0.000 |           2.209 / 0.000 |

### Sample Size: 1 billion (15G)

| Solution                                                  | CPython AET/VAR | CPython_PerfOpt AET/VAR |
| :-------------------------------------------------------- | --------------: | ----------------------: |
| `06_polars_read_csv`                                      |          KILLED |                  KILLED |
| `06_polars_scan_csv`                                      |          KILLED |                  KILLED |
| `06_polars_scan_csv_streaming`                            |  28.415 / 0.015 |          28.200 / 0.482 |
| `07_duckdb`                                               |  30.683 / 0.610 |          30.233 / 1.093 |
| `07_duckdb_parallel`                                      |  31.040 / 0.134 |          31.231 / 0.242 |
| `09_pyarrow`                                              |          KILLED |                  KILLED |
| `10_parquet_polars_read_parquet` (uncompressed)           |          KILLED |                  KILLED |
| `10_parquet_polars_scan_parquet` (uncompressed)           |          KILLED |                  KILLED |
| `10_parquet_polars_scan_parquet_streaming` (uncompressed) |  20.310 / 0.031 |          20.323 / 0.016 |
| `10_parquet_duckdb` (uncompressed)                        |  15.693 / 0.001 |          15.695 / 0.001 |
| `10_parquet_pyarrow` (uncompressed)                       |          KILLED |                  KILLED |
| `10_parquet_pyarrow_memory_map` (uncompressed)            |          KILLED |                  KILLED |
| `10_parquet_polars_read_parquet` (lz4)                    |          KILLED |                  KILLED |
| `10_parquet_polars_scan_parquet` (lz4)                    |          KILLED |                  KILLED |
| `10_parquet_polars_scan_parquet_streaming` (lz4)          |  21.260 / 0.006 |          21.244 / 0.006 |
| `10_parquet_duckdb` (lz4)                                 |  16.384 / 0.001 |          16.372 / 0.000 |
| `10_parquet_pyarrow` (lz4)                                |          KILLED |                  KILLED |
| `10_parquet_pyarrow_memory_map` (lz4)                     |          KILLED |                  KILLED |
| `11_duckdb_duckdb`                                        |  12.626 / 0.256 |          12.647 / 0.629 |

### Conditions

- Python version: 3.12.3
  - Exception: `05_modin_ray` uses 3.11.9 because `ray` needs it
- CPU: 12th Gen Intel® Core™ i7-1255U × 12
- RAM: 16.0 GiB
- Hard Drive: WD PC SN560 SDDPNQE-1T00-1006 (SSD)
- All benchmarks are executed inside docker containers
  - To avoid any performance penalty due to docker security features, the `--privileged` flag is used when running the container (suggested by Python⇒Speed [here](https://pythonspeed.com/articles/docker-performance-overhead/))
  - Please refer to the `./scripts/docker_run_*.sh` scripts to see exactly how tests are executed under docker containers

## Approaches Description

- `00_native_DictReader`: reads `DictReader` item by item, updating an accumulator dict iteratively
- `00_native_DictReader_no_gc`:  variant of `00_native_DictReader` with garbage collection disabled
- `01_native_split`: reads from `Path.open()` line by line, splitting the line by ";" and updating an accumulator dict iteratively
- `01_native_split_no_gc`:  variant of `01_native_split` with garbage collection disabled
- `02_native_read_text`: uses `Path.read_text()` to load the entire file at once, splitting by "\n" and then by ";", and finally updating an accumulator dict iteratively
- `02_native_read_text_no_gc`: variant of `02_native_read_text` with garbage collection disabled
- `03_pandas`: uses the [pandas](https://pypi.org/project/pandas/) library; reads the csv data with `pandas.read_csv()`, then uses `df.groupby()` to group the stations, and finally aggregates the temperatures with `df_gb.agg(["min", "mean", "max"])`
- `03_pandas_pyarrow`: variant of `03_pandas` that uses the newer [pyarrow](https://pypi.org/project/pyarrow/) engine
- `04_dask`: uses the [dask](https://pypi.org/project/dask/) library for parallel computing (mirrors `03_pandas` implementation)
- `04_dask_pyarrow`: variant of `04_dask` that uses the newer [pyarrow](https://pypi.org/project/pyarrow/) engine
- `05_modin_ray`: uses the [modin](https://pypi.org/project/modin/) library with the [ray](https://pypi.org/project/ray/) framework to scale pandas workflows (mirrors `03_pandas` implementation)
- `06_polars_read_csv`: uses the [polars](https://pypi.org/project/polars/) library, designed for efficient data manipulation and analysis using [Rust](https://www.rust-lang.org/) and [Apache Arrow Columnar Format](https://arrow.apache.org/docs/format/Columnar.html); reads the entire csv data into memory with `pl.read_csv()`, then uses `df.group_by()` to group the stations, and finally aggregates the temperatures with `df_gb.agg(min, mean, max)`
- `06_polars_scan_csv`: variant of `06_polars_read_csv` that uses `pl.scan_csv()` instead of `pl.read_csv()` for a lazy evaluation
- `06_polars_scan_csv_streaming`: variant of `06_polars_scan_csv` that uses `collect(streaming=True)` to process the query in batches to handle larger-than-memory data
- `07_duckdb`: uses [duckdb](https://duckdb.org/) as an in-process analytical database; reads the csv data through `duckdb.read_csv()` and then simply groups and aggregates for `min, avg, max`
- `07_duckdb_parallel`: variant of `07_duckdb` that uses `duckdb.read_csv(parallel=True)` for parallel processing (experimental feature)
- `08_numpy`: reads the csv data with `pandas.read_csv()`, converts the dataframe using `df.to_numpy()`, computes the unique stations, iterates over each unique one, filters the data for it, and then calculates the min, average, and max
- `09_pyarrow`: uses the [pyarrow](https://pypi.org/project/pyarrow/) engine to read the csv with `pyarrow.csv.read_csv()`, groups by station, aggregates for `min, avg, max`, and finally joins all columns into a single one
- `10_parquet_polars_read_parquet`: same approach as `06_polars_read_csv`, but uses a parquet file instead of a CSV
- `10_parquet_polars_scan_parquet`: same approach as `06_polars_scan_csv`, but uses a parquet file instead of a CSV
- `10_parquet_polars_scan_parquet_streaming`: same approach as `06_polars_scan_csv_streaming`, but uses a parquet file instead of a CSV
- `10_parquet_duckdb`: same approach as `07_duckdb`, but uses a parquet file instead of a CSV
- `10_parquet_pyarrow`: same approach as `09_pyarrow`, but uses a parquet file instead of a CSV
- `10_parquet_pyarrow_memory_map`: variant of `10_parquet_pyarrow` that uses `read_table(memory_map=True)` to try to increase performance
- `11_duckdb_duckdb`: same approach as `07_duckdb`, but uses a duckdb file instead of a CSV

### Python Implementations

- **CPython**: the standard, vanilla Python implemented in C
- **CPython_PerfOpt**: same as CPython, but compiled and built with the following flags to optimize for performance (as per the [Python Developer's Guide](https://devguide.python.org/getting-started/setup-building/index.html#optimization)):
  - [`--enable-optimizations`](https://docs.python.org/3/using/configure.html#cmdoption-enable-optimizations) (enables Profile Guided Optimization)
  - [`--with-lto`](https://docs.python.org/3/using/configure.html#cmdoption-with-lto) (enables Link Time Optimization)
