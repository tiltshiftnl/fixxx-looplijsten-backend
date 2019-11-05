#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

echo Collecting static files
python manage.py collectstatic --no-input

ls -al /static/

chmod -R 777 /static

# run uwsgi
exec uwsgi --ini settings/uwsgi.ini >> /var/log/uwsgi/uwsgi.log 2>&1
