# onebrc

![Python](https://img.shields.io/badge/python-006d98?style=for-the-badge&logo=python&logoColor=ffc600)
![Docker](https://img.shields.io/badge/docker-2496ed?style=for-the-badge&logo=docker&logoColor=ffffff)

This repository contains various approaches to solve [1️⃣🐝🏎️ The One Billion Row Challenge](https://github.com/gunnarmorling/onebrc) using the Python ecosystem.
Contrary to the rules of the challenge, external dependencies are used.

## Execution Benchmarks

Next follows a table with benchmarks for all solutions.
These benchmarks are the Average Execution Time (AET) in seconds for 10 executions.
Please refer to [exec_logs](./exec_logs/) for the execution log of these benchmarks.
It is possible for each solution to be applied to different constraints, such as Python implementations.
Please refer to [Python Implementations](#python-implementations) for more information on the variants used.
The sample size is 100_000_000.

| Solution                       |          CPython AET | CPython_PerfOpt AET | CPython_PerfOpt NoGC AET |
| :----------------------------- | -------------------: | ------------------: | -----------------------: |
| `00_native_DictReader`         | 103.5024992948000000 | 84.7618062428001300 |       84.535680547699940 |
| `01_native_split`              |  40.4640003209999600 | 34.2665251072999100 |       34.461449691899910 |
| `02_native_read_text`          |  43.9490607891999400 | 40.3054384241000700 |       38.031868851099986 |
| `03_pandas`                    |  23.9660524116000500 | 21.5296436360998100 |                       NA |
| `03_pandas_pyarrow`            |   8.8102804387000100 |  8.3487482031000580 |                       NA |
| `04_dask`                      |  17.6968689788996940 | 17.0897760238998660 |                       NA |
| `04_dask_pyarrow`              |   7.4737623227994850 |  7.4544295981995670 |                       NA |
| `05_modin_ray`                 |  26.5887451761998830 | 24.7589070680000060 |                       NA |
| `06_polars_read_csv`           |   4.8700010490000750 |  4.8267042113001480 |                       NA |
| `06_polars_scan_csv`           |   5.1010372745000490 |  4.8729900201999050 |                       NA |
| `06_polars_scan_csv_streaming` |   2.9765750913000373 |  2.9723517919000186 |                       NA |
| `07_duckdb`                    |   2.2371692372002143 |  2.2268917563000286 |                       NA |
| `07_duckdb_parallel`           |   2.5806502976003687 |  2.5366062677998342 |                       NA |

### Conditions

- Python version: 3.12.3
  - Exception: `04_modin` uses 3.11.9 because `ray` needs it
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
- `07_duckdb_parallel`: variant of `07_duckdb` that uses `duckdb.read_csv(parallel=True)` for parallel processing

### Python Implementations

- **CPython**: the standard, vanilla Python implemented in C
- **CPython_PerfOpt**: same as CPython, but compiled and built with the following flags to optimize for performance (as per the [Python Developer's Guide](https://devguide.python.org/getting-started/setup-building/index.html#optimization)):
  - [`--enable-optimizations`](https://docs.python.org/3/using/configure.html#cmdoption-enable-optimizations) (enables Profile Guided Optimization)
  - [`--with-lto`](https://docs.python.org/3/using/configure.html#cmdoption-with-lto) (enables Link Time Optimization)
