#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

echo Collecting static files
python manage.py collectstatic --no-input

ls -al /static/

chmod -R 777 /static

# modify permission so scoring files can be cached
chmod -R 700 /fraud_prediction_cache

# run uwsgi
cd /app/
exec uwsgi
