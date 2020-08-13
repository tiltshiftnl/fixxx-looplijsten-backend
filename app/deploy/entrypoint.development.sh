# Same as entrypoint.sh, but with py-auto-reload enabled to allow auto reloading when making changes during development

#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

echo Collecting static files
python manage.py collectstatic --no-input

yes yes | python manage.py migrate --noinput

chmod -R 777 /static

# modify permission so scoring files can be cached
chmod -R 700 /fraud_prediction_cache

# run uwsgi
exec uwsgi --ini /app/deploy/config.ini --py-auto-reload=1 --cheaper-initial=1 --cheaper=1 --processes=10
