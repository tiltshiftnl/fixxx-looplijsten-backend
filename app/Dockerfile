FROM amsterdam/python
LABEL maintainer="datapunt@amsterdam.nl"

ENV PYTHONUNBUFFERED 1

RUN adduser --system datapunt

RUN mkdir -p /static && chown datapunt /static
RUN mkdir -p /app && chown datapunt /app
RUN mkdir -p /downloads && chown datapunt /downloads
RUN mkdir -p /certificates && chown datapunt /certificates
RUN mkdir -p /deploy && chown datapunt /deploy
RUN mkdir -p /var/log/uwsgi && chown datapunt /var/log/uwsgi

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
USER datapunt

COPY . /app/
COPY deploy /deploy/

CMD ["/deploy/docker-run.sh"]