#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

docker run --privileged --rm -it -m=16gb --shm-size=16gb \
    -v /home/oceord/Dev/1brc-python/test_data:/onebrc/test_data \
    --name onebrc-cpython_perf onebrc-cpython_perf \
    make run-duckdb_db-1b-docker | tee "$SCRIPT_DIR/../../exec_logs/1b/CPython_PerfOpt_DuckDB_DB.txt"
