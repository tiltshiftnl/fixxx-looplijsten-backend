FROM rust:1.40 as pg_anonymize
WORKDIR /app
COPY pg_anonymize/ .
RUN cargo build --release

FROM ubuntu:latest

RUN apt-get update && apt-get install -y cron postgresql-client

COPY --from=pg_anonymize /app/target/release/pg_anonymize /usr/local/bin/
COPY pg_anonymize.conf /etc/

COPY bwv-sync.cron /etc/cron.d/bwv-sync
RUN chmod 0644 /etc/cron.d/bwv-sync
RUN crontab /etc/cron.d/bwv-sync

COPY bwv-sync.sh /usr/local/bin/looplijsten_bwv_sync.sh
RUN chmod 755 /usr/local/bin/looplijsten_bwv_sync.sh

RUN touch /var/log/cron.log

CMD ["cron", "-f"]
