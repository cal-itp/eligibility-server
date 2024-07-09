#!/usr/bin/env bash
set -eu

git config --global --add safe.directory /home/compiler/site

pre-commit install --install-hooks
