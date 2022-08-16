#!/usr/bin/env bash
set -eux

# initialize the application database
python setup.py

# initialize hook environments
pre-commit install --install-hooks --overwrite
