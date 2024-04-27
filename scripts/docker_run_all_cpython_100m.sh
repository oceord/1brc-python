#!/usr/bin/env bash

docker run --privileged --rm -v /home/oceord/Dev/1brc-python/test_data:/onebrc/test_data -it --name onebrc-cpython onebrc-cpython make run-cpython-100m-docker
