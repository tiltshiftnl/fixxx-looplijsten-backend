#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x   # print what we are doing

/deploy/docker-wait.sh
/deploy/docker-migrate.sh

python manage.py test