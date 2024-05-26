#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

for SCRIPT in "$SCRIPT_DIR"/200m/*.sh; do
    if [ -f "$SCRIPT" ]; then
        bash "$SCRIPT"
        sleep 60
    fi
done
