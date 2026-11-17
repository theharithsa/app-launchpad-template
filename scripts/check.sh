#!/bin/sh
set -eu
cd "$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
"${PYTHON:-python3}" scripts/check_foundation.py
"${PYTHON:-python3}" scripts/check_links.py
"${PYTHON:-python3}" scripts/check_docs_impact.py
"${PYTHON:-python3}" scripts/build_public_docs.py
"${PYTHON:-python3}" -m unittest discover -s tests -v
