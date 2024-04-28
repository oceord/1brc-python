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

| Solution               |        CPython AET | CPython_PerfOpt AET | CPython_PerfOpt NoGC AET |
| :--------------------- | -----------------: | ------------------: | -----------------------: |
| `00_native_DictReader` | 103.50249929480000 |   84.76180624280013 |       84.535680547699940 |
| `01_native_split`      |  40.46400032099996 |   34.26652510729991 |       34.461449691899910 |
| `02_native_read_text`  |  43.94906078919994 |   40.30543842410007 |       38.031868851099986 |

### Conditions

- Python version: 3.12.3
- CPU: 12th Gen Intel® Core™ i7-1255U × 12
- RAM: 16.0 GiB
- Hard Drive: WD PC SN560 SDDPNQE-1T00-1006 (SSD)
- All benchmarks are executed inside docker containers
  - To avoid any performance penalty due to docker security features, the `--privileged` flag is used when running the container (suggested by Python⇒Speed [here](https://pythonspeed.com/articles/docker-performance-overhead/))
  - Please refer to the `./scripts/docker_run_*.sh` scripts to see exactly how tests are executed under docker containers

## Approaches Description

- `00_native_DictReader`: read `DictReader` item by item, updating an accumulator dict iteratively
- `00_native_DictReader_no_gc`:  variant of `00_native_DictReader` with garbage collection disabled
- `01_native_split`: read from `Path.open()` line by line, splitting the line by ";" and updating an accumulator dict iteratively
- `01_native_split_no_gc`:  variant of `01_native_split` with garbage collection disabled
- `02_native_read_text`: use `Path.read_text()` to load the entire file at once, splitting by "\n" and then by ";", and finally updating an accumulator dict iteratively
- `02_native_read_text_no_gc`: variant of `02_native_read_text` with garbage collection disabled

### Python Implementations

- **CPython**: the standard, vanilla Python implemented in C
- **CPython_PerfOpt**: same as CPython, but compiled and built with the following flags to optimize for performance (as per the [Python Developer's Guide](https://devguide.python.org/getting-started/setup-building/index.html#optimization)):
  - [`--enable-optimizations`](https://docs.python.org/3/using/configure.html#cmdoption-enable-optimizations) (enables Profile Guided Optimization)
  - [`--with-lto`](https://docs.python.org/3/using/configure.html#cmdoption-with-lto) (enables Link Time Optimization)
