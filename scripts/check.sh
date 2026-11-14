#!/bin/sh
set -eu
cd "$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
python3 scripts/check_foundation.py
python3 scripts/check_links.py
python3 scripts/check_docs_impact.py
python3 scripts/build_public_docs.py
python3 -m unittest discover -s tests -v
