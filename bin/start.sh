#! usr/bin/env bash
set -eux

# initialize Flask

bin/init.sh

# start the web server

flask run -h 0.0.0.0
