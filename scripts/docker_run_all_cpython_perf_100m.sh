#!/usr/bin/env bash

docker run --privileged --rm -v /home/oceord/Dev/1brc-python/test_data:/onebrc/test_data -it --name onebrc-cpython_perf onebrc-cpython_perf make run-cpython-docker-100m
