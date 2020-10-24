# locust_exporter
A locust exporter for prometheus.

Currently works with:
- Locust v1.2.3
  - https://github.com/locustio/locust
- Prometheus client_python v0.8.0
  - https://github.com/prometheus/client_python

This is a simple exporter for http://locust.io metrics. You get all the necessary details about current tests and the state of the locust.

Errors and requests stats are added with the method and path labels - BE CAREFUL - if you have a lot of endpoints. It is probably better to group the endpoints in your locustfile (please see: http://docs.locust.io/en/latest/writing-a-locustfile.html#grouping-requests-to-urls-with-dynamic-parameters).

Requirements: prometheus_client (sudo pip install prometheus_client)

Running the exporter:

`./locust_exporter.py <listen_port> <locust_host:port>`

i.e.:

`./locust_exporter.py 1234 localhost:8089`

