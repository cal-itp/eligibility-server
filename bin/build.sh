#!/usr/bin/env bash
set -eux

# if on Apple M1
# https://stackoverflow.com/a/65259353/358804
if [[ $(uname -m) == 'arm64' ]]; then
    # workaround for an issue in BuildKit causing dependent builds (specifically the dev image) to fail
    # https://github.com/docker/compose/issues/8449#issuecomment-1125761231
    export DOCKER_BUILDKIT=0

    # disable buildkit in the devcontainer
    # https://github.com/microsoft/vscode-remote-release/issues/1409#issuecomment-666240303
    # https://stackoverflow.com/a/3557165/358804
    grep -qF 'DOCKER_BUILDKIT' .env || echo 'DOCKER_BUILDKIT=0' >> .env
fi

docker compose build --pull server

docker compose build dev
