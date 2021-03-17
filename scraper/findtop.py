from prometheus_api_client import PrometheusConnect,  MetricSnapshotDataFrame, MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta
from metricshandler import queryMetrics

import pandas as pd
prom = PrometheusConnect(url ="http://localhost:9090", disable_ssl=True)

from datetime import timedelta

def top3_latency():
    # print("\n TOP3 LATENCY START\n")
    latency = "sum(irate(istio_request_duration_milliseconds_sum{reporter='source'}[1m])) by (source_app, destination_app) / sum(irate(istio_request_duration_milliseconds_count{reporter='source', destination_app!='unknown'}[1m])) by (source_app, destination_app)"
    head = 3
    metric_data = queryMetrics(latency, head)
    
    # print("\n *************     %s     *************\n" % (latency))
    # print(metric_data)
    apps = ""
    topLatencyServices = []
    for i in range(0, len(metric_data),1):
        metricTuple = metric_data.iloc[i] 
        topLatencyServices.append(metricTuple[0])
    print("Top 3 latency:\n")            
    print(topLatencyServices)
    # print("\n TOP3 LATENCY END\n")
    return topLatencyServices
    # return destination_app