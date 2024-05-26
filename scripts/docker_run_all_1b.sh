#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

for SCRIPT in "$SCRIPT_DIR"/1b/*.sh; do
    if [ -f "$SCRIPT" ]; then
        bash "$SCRIPT"
        sleep 60
    fi
done
