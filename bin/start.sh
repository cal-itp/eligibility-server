#! usr/bin/env bash
set -eux

# initialize Flask

bin/init.sh

# start the web server

nginx

python -m gunicorn -c $GUNICORN_CONF eligibility_server.app:app
