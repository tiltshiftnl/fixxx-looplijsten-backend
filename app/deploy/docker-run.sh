#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

echo Run tests
yes yes | python manage.py test --noinput

echo Collecting static files
python manage.py collectstatic --no-input

yes yes | python manage.py migrate --noinput

chmod -R 777 /static

# modify permission so scoring files can be cached
chmod -R 700 /fraud_prediction_cache

# run uwsgi
cd /app/
exec uwsgi
