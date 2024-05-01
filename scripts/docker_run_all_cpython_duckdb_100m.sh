#!/usr/bin/env bash

docker run --privileged --rm -it \
    -v /home/oceord/Dev/1brc-python/test_data:/onebrc/test_data \
    --name onebrc-cpython onebrc-cpython \
    make run-duckdb-100m-docker
