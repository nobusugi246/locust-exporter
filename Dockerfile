FROM python:3.8

RUN pip install --no-cache-dir prometheus_client

ARG user=locust
ARG group=locust
ARG uid=1000
ARG gid=1000
ARG HOME=/home/locust

RUN groupadd -g ${gid} ${group} \
    && useradd -d "$HOME" -u ${uid} -g ${group} -m -s /bin/bash ${user} \
    && mkdir -p $HOME \
    && chown ${uid}:${gid} $HOME

USER ${user}

COPY locust_exporter.py $HOME
CMD  $HOME/locust_exporter.py 1234 localhost:8089
