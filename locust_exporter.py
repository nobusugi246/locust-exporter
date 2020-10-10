#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Requires prometheus_client library:
# sudo pip install prometheus_client
from prometheus_client import start_http_server, Metric, REGISTRY
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
import json
import requests
import sys
import time

class LocustCollector(object):
  def __init__(self, ep):
    self._ep = ep

  def collect(self):
    # Fetch the JSON
    url = 'http://' + self._ep + '/stats/requests'
    try:
        response = requests.get(url).content.decode('Utf-8')
    except requests.exceptions.ConnectionError:
        print("Failed to connect to Locust:", url)
        exit(2)

    response = json.loads(response)

    yield GaugeMetricFamily('locust_user_count', 'Swarmed users', value=response['user_count'])

    for err in response['errors']:
        metric = GaugeMetricFamily('locust_errors', 'Locust requests errors', labels=['path', 'method'])
        metric.add_metric([str(err['name']), str(err['method'])], value=err['occurences'])
        yield metric

    if 'slave_count' in response:
        yield GaugeMetricFamily('locust_slave_count', 'Locust number of slaves', value=response['slave_count'])

    yield GaugeMetricFamily('locust_fail_ratio', 'Locust failure ratio', value=response['fail_ratio'])

    metric = GaugeMetricFamily('locust_state', 'State of the locust swarm', labels=['state'])
    metric.add_metric([str(response['state'])], 1)
    yield metric

    stats_metrics_gause = ['avg_content_length','avg_response_time','current_rps','max_response_time','median_response_time','min_response_time']
    stats_metrics_count = ['num_failures','num_requests']
    for mtr in stats_metrics_gause:
        metric = GaugeMetricFamily('locust_requests_' + mtr, 'locust requests ' + mtr, labels=['path', 'method'])
        for stat in response['stats']:
            if not 'Total' in stat['name']:
                metric.add_metric([str(stat['name']), str(stat['method'])], stat[mtr])
        yield metric
    for mtr in stats_metrics_count:
        metric = CounterMetricFamily('locust_requests_' + mtr, 'locust requests ' + mtr, labels=['path', 'method'])
        for stat in response['stats']:
            if not 'Total' in stat['name']:
                metric.add_metric([str(stat['name']), str(stat['method'])], stat[mtr])
        yield metric


if __name__ == '__main__':
  # Usage: locust_exporter.py <port> <locust_host:port>
  if len(sys.argv) != 3:
      print('Usage: locust_exporter.py <port> <locust_host:port>')
      exit(1)
  else:
    try:
        start_http_server(int(sys.argv[1]))
        REGISTRY.register(LocustCollector(str(sys.argv[2])))
        print("Connecting to locust on: " + sys.argv[2])
        while True: time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
