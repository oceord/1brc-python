#!/usr/bin/env bash

docker run --privileged --rm -it --shm-size=8gb \
    -v /home/oceord/Dev/1brc-python/test_data:/onebrc/test_data \
    --name onebrc-cpython_perf-modin onebrc-cpython_perf-modin \
    make run-modin-ray-100t-docker
