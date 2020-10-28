FROM rust:1.40 as pg_anonymize
WORKDIR /app
COPY pg_anonymize/ .

# Setup Certificates for ADP/Motiv
COPY ./certificates/adp_rootca.crt /usr/local/share/ca-certificates/extras/adp_rootca.crt
RUN chmod 644 /usr/local/share/ca-certificates/extras/adp_rootca.crt \
  && update-ca-certificates --fresh

RUN cargo build --release

FROM ubuntu:latest

RUN apt-get update && apt-get install -y cron postgresql-client curl tzdata

COPY --from=pg_anonymize /app/target/release/pg_anonymize /usr/local/bin/
COPY pg_anonymize.conf /etc/

COPY bwv-sync.cron /etc/cron.d/bwv-sync
RUN chmod 0644 /etc/cron.d/bwv-sync
RUN crontab /etc/cron.d/bwv-sync

COPY bwv-sync.sh /usr/local/bin/looplijsten_bwv_sync.sh
RUN chmod 755 /usr/local/bin/looplijsten_bwv_sync.sh

COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh

RUN touch /var/log/cron.log

ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD /entrypoint.sh
