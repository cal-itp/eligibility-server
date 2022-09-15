#!/usr/bin/env bash
set -eux

docker compose build --pull server

docker compose build dev
