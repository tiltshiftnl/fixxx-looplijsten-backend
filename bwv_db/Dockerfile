FROM amsterdam/postgres11

ENV SQL_DIR=/bwv_sql

COPY sql/*.sql ${SQL_DIR}/
COPY init_db.sh /docker-entrypoint-initdb.d/
