FROM python:3.8-slim

RUN pip install --no-cache-dir prometheus_client

ARG user=operator
ARG uid=1000
ARG HOME=/home/operator

RUN mkdir -p $HOME \
    && useradd -d "$HOME" -u ${uid} -g operator -m -s /bin/bash ${user} \
    && chown operator:operator $HOME

USER ${user}

COPY locust_exporter.py $HOME
CMD  $HOME/locust_exporter.py 1234 localhost:8089
