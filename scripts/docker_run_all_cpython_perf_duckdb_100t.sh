#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

docker run --privileged --rm -it --shm-size=8gb \
    -v /home/oceord/Dev/1brc-python/test_data:/onebrc/test_data \
    --name onebrc-cpython_perf onebrc-cpython_perf \
    make run-duckdb-100t-docker | tee "$SCRIPT_DIR/../exec_logs/CPython_PerfOpt_DuckDB.log"