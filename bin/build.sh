#!/usr/bin/env bash
set -eux

docker compose build server

docker compose build dev
