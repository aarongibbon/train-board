#!/bin/bash
exec > /tmp/station-board.autostart.log 2>&1
SCRIPT_DIR=$(dirname "$0")
pushd $SCRIPT_DIR
echo $pwd
python3 src/main.py

