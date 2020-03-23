#!/usr/bin/env bash
#
# This script will sync the local looplijsten_bwv database from views in the
# data analytics wonen database. It is meant to run from cron. The local tables
# will be TRUNCATE-d before the sync. The views don't contain a lot of data so
# the sync doesn't take long.

# Let's make it easy to ourselves and prevent bash from interpreting the '*' in
# 'select * from ...'
set -o noglob
set -euo pipefail

src_host=swdbmams2204.basis.lan
src_db=rve_wonen
src_user=srvc_fixxx
src_pw="${RVE_WONEN_PASSWORD}"
dst_db="${BWV_DB_NAME}"
if test "${ENVIRONMENT}" = "acceptance"; then
anonymize=true
else
anonymize=false
fi
logfile="/tmp/bwv-sync.log"

# The views/tables to sync and the table to sync them to.
# Format: <source view/table>,<destination table>
tables=(
  view_benb_meldingen,bwv_benb_meldingen
  view_hotline_bevinding,bwv_hotline_bevinding
  view_hotline_melding,bwv_hotline_melding
  view_import_adres,import_adres
  view_import_stadia,import_stadia
  view_import_wvs,import_wvs
  view_medewerkers,bwv_medewerkers
  view_personen,bwv_personen
  view_personen_hist,bwv_personen_hist
  view_vakantieverhuur,bwv_vakantieverhuur
  view_woningen,bwv_woningen
)

export PGPASSWORD="${src_pw}"
for src_dst in ${tables[@]}; do
  src_table=$(cut -d, -f 1 <<<"$src_dst")
  dst_table=$(cut -d, -f 2 <<<"$src_dst")
  echo "Syncing $src_table on ${src_host}:${src_db} to $dst_table" | tee "$logfile"

  PGPASSWORD="${BWV_DB_PASSWORD}" psql -h "${BWV_DB_HOST}" -U "${BWV_DB_USER}" -c "TRUNCATE $dst_table" "$dst_db"
  psql --no-align --tuples-only -h "$src_host" -d "$src_db" -U "$src_user" \
    -c "COPY (SELECT * FROM $src_table) TO STDOUT" \
    | if $anonymize; then /usr/local/bin/pg_anonymize -c /etc/pg_anonymize.conf "$dst_table"; else cat -; fi \
    | PGPASSWORD="${BWV_DB_PASSWORD}" psql -h "${BWV_DB_HOST}" -U "${BWV_DB_USER}" -d "$dst_db" -c "COPY $dst_table FROM STDIN"
done
