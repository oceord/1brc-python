#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

docker run --privileged --rm -it -m=16gb --shm-size=16gb \
    -v /home/oceord/Dev/1brc-python/test_data:/onebrc/test_data \
    --name onebrc-cpython_perf-modin onebrc-cpython_perf-modin \
    make run-modin-ray-100m-docker | tee "$SCRIPT_DIR/../../exec_logs/100m/CPython_PerfOpt_Modin.txt"
