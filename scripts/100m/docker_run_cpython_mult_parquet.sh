#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

docker run --privileged --rm -it -m=16gb --shm-size=16gb \
    -v /home/oceord/Dev/1brc-python/test_data:/onebrc/test_data \
    --name onebrc-cpython onebrc-cpython \
    make run-mult_parquet_duckdb-100m-docker | tee "$SCRIPT_DIR/../../exec_logs/100m/CPython_Mult_Parquet.txt"
