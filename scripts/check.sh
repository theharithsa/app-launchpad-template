#!/bin/sh
set -eu
cd "$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
python3 scripts/check_foundation.py
python3 scripts/check_links.py
python3 -m unittest discover -s tests -v
