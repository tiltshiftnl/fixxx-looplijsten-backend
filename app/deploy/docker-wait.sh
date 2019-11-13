#!/usr/bin/env bash

set -u
set -e

# wait for postgres
while ! nc -z $DATABASE_HOST $DATABASE_PORT
do
	echo "Waiting for postgres db @ $DATABASE_HOST:$DATABASE_PORT.."
	sleep 2
done