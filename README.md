# onebrc

![Python](https://img.shields.io/badge/python-006d98?style=for-the-badge&logo=python&logoColor=ffc600)
![Docker](https://img.shields.io/badge/docker-2496ed?style=for-the-badge&logo=docker&logoColor=ffffff)

This repository contains various attempts to solve the [1brc](https://github.com/gunnarmorling/onebrc) challenge through Python (external dependencies are used).

## Execution Benchmarks

Next follows a table with benchmarks for all approaches.
Benchmarks are calculated as the average time (in seconds) of 10 executions.
Please refer to [EXEC.log](./EXEC.log) for the execution log of these benchmarks.
The sample size is 100_000_000.

| Module                 | AvgExecTime (CPython) |
| :--------------------- | --------------------: |
| `00_native_DictReader` |     95.10874163000008 |
| `01_native_split`      |     37.37240671530003 |
| `02_native_read_text`  |     43.90962733860001 |

**Conditions**:

- CPU: 12th Gen Intel® Core™ i7-1255U × 12
- RAM: 16.0 GiB
- All benchmarks are executed inside a docker container. To avoid any performance penalty due to docker security features, the `--privileged` flag is used when running the container, as suggested by [this](https://pythonspeed.com/articles/docker-performance-overhead/) Python⇒Speed article. Please refer to the `./scripts/docker_run_*.sh` scripts to see exactly how tests are executed under docker.

## Description

- `00_native_DictReader`: read DictReader item by item, updating an accumulator dict iteratively
- `01_native_split`: read from Path.open() line by line, splitting the line by ";" and updating an accumulator dict iteratively
- `02_native_read_text`: use Path.read_text() to load the entire file at once, splitting by "\n" and then by ";", and finally updating an accumulator dict iteratively
