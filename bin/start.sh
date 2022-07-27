#! usr/bin/env bash
set -eux

python setup.py

flask run -h 0.0.0.0
