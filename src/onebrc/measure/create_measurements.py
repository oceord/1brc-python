#!/usr/bin/env python
#
#  Copyright 2023 The original authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Based on https://github.com/gunnarmorling/onebrc/blob/main/src/main/java/dev/morling/onebrc/CreateMeasurements.java

import os
import random
import sys
import time
from importlib.resources import files
from math import ceil
from pathlib import Path

SCRIPT_DIR = Path(os.path.realpath(__file__)).parent
WEATHER_STATIONS_IO = files("onebrc.measure.data").joinpath("weather_stations.csv")
OUTPUT_FILE = Path("test_data/measurements.txt")


def build_weather_station_name_list():
    """Grabs the weather station names from example data provided in repo and dedups."""
    station_names = []
    with WEATHER_STATIONS_IO.open() as file:
        file_contents = file.read()
        station_names = [
            station.split(";")[0]
            for station in file_contents.splitlines()
            if "#" not in station
        ]
    return list(set(station_names))


def convert_bytes(num):
    """Convert bytes to a human-readable format (e.g., KiB, MiB, GiB)."""
    for x in ["bytes", "KiB", "MiB", "GiB"]:
        base = 1024.0
        if num < base:
            return f"{num:3.1f} {x}"
        num /= base
    return None


def format_elapsed_time(seconds):
    """Format elapsed time in a human-readable format."""
    sec_in_min = 60
    sec_in_hour = 3600
    if seconds < sec_in_min:
        return f"{seconds:.3f} seconds"
    elif seconds < sec_in_hour:  # noqa: RET505
        minutes, seconds = divmod(seconds, sec_in_min)
        return f"{int(minutes)} minutes {int(seconds)} seconds"
    else:
        hours, remainder = divmod(seconds, sec_in_hour)
        minutes, seconds = divmod(remainder, sec_in_min)
        if minutes == 0:
            return f"{int(hours)} hours {int(seconds)} seconds"
        return f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"


def estimate_file_size(weather_station_names, num_rows_to_create):
    """Tries to estimate how large a file the test data will be."""
    total_name_bytes = sum(len(s.encode("utf-8")) for s in weather_station_names)
    avg_name_bytes = total_name_bytes / float(len(weather_station_names))

    avg_temp_bytes = 4.400200100050025

    # add 2 for separator and newline
    avg_line_length = avg_name_bytes + avg_temp_bytes + 2

    human_file_size = convert_bytes(num_rows_to_create * avg_line_length)

    return f"Estimated max file size is:  {human_file_size}."


def build_test_data(weather_station_names, num_rows_to_create):
    """Generates and writes to file the requested length of test data."""
    start_time = time.time()
    coldest_temp = -99.9
    hottest_temp = 99.9
    station_names_10k_max = random.choices(weather_station_names, k=10_000)
    batch_size = 100000
    chunks = ceil(num_rows_to_create / batch_size)
    print("Building test data...")

    try:
        with Path(OUTPUT_FILE).open("w") as file:
            progress = 0
            for chunk in range(chunks):

                batch = random.choices(station_names_10k_max, k=batch_size)
                prepped_deviated_batch = "\n".join(
                    [
                        f"{station};{random.uniform(coldest_temp, hottest_temp):.1f}"
                        for station in batch
                    ],
                )  # :.1f should quicker than round on a large scale,
                #       because round utilizes mathematical operation
                file.write(prepped_deviated_batch + "\n")

                # Update progress bar every 1%
                if (chunk + 1) * 100 // chunks != progress:
                    progress = (chunk + 1) * 100 // chunks
                    bars = "=" * (progress // 2)
                    sys.stdout.write(f"\r[{bars:<50}] {progress}%")
                    sys.stdout.flush()
        sys.stdout.write("\n")
    except Exception as e:
        print("Something went wrong. Printing error info and exiting...")
        print(e)
        sys.exit()

    end_time = time.time()
    elapsed_time = end_time - start_time
    file_size = Path(OUTPUT_FILE).stat().st_size
    human_file_size = convert_bytes(file_size)

    print("Test data successfully written to onebrc/data/measurements.txt")
    print(f"Actual file size:  {human_file_size}")
    print(f"Elapsed time: {format_elapsed_time(elapsed_time)}")


def create_measurement_file(num_rows_to_create):
    """Main program function."""
    weather_station_names = build_weather_station_name_list()
    print(estimate_file_size(weather_station_names, num_rows_to_create))
    build_test_data(weather_station_names, num_rows_to_create)
    print("Test data build complete.")


if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    create_measurement_file(size)
