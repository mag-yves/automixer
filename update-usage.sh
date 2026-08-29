#!/usr/bin/env bash
set -euo pipefail

cd /media/yves/SSD4TO/pro/automixer

python3 update_usage.py "$@"
