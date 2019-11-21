#!/usr/bin/env bash
#
# Initialize the looplijsten_bwv database.
set -euo pipefail

DB_NAME=looplijsten_bwv
DB_USER=looplijsten_bwv
PSQL="psql --username $POSTGRES_USER"

# Create the user & database. The `|| true` is to prevent errors if they
# already exists, which can happen if docker-compose has already created them.
$PSQL <<EOF || true
  CREATE USER $DB_USER;
  CREATE DATABASE $DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

# Run the scripts to create the schema
for f in ${SQL_DIR}/*.sql; do
  $PSQL --dbname "$DB_NAME" -f "$f"
done
