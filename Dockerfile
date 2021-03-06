FROM ghcr.io/deephaven/server:edge AS ts-server
COPY data/app.d /app.d
HEALTHCHECK --interval=3s --retries=3 --timeout=11s CMD /bin/grpc_health_probe -addr=localhost:8080 -connect-timeout=10s || exit 1

FROM ghcr.io/deephaven/web:edge AS ts-web
COPY data/notebooks /data/notebooks
RUN chown www-data:www-data /data/notebooks

from python:3.8 AS twitter-sent
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
