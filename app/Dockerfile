FROM amsterdam/python
LABEL maintainer="datapunt@amsterdam.nl"

ENV PYTHONUNBUFFERED 1

# Setup Certificates for ADP/Motiv
COPY certificates/adp_rootca.crt /usr/local/share/ca-certificates/extras/adp_rootca.crt
RUN chmod 644 /usr/local/share/ca-certificates/extras/adp_rootca.crt \
  && update-ca-certificates --fresh

# Setup datapunt directories and user
RUN adduser --system datapunt
ENV DIRECTORYLIST "/static /app /downloads /certificates /deploy /var/log/uwsgi /fraud_prediction_cache"
RUN mkdir -p ${DIRECTORYLIST} && chown datapunt ${DIRECTORYLIST}

# Setup application
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
USER datapunt

COPY . /app/
COPY deploy /deploy/

CMD ["/deploy/docker-run.sh"]
