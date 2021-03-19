# myconfig.py:

metricQuery_error = "sum(rate(istio_requests_total{reporter='source',MY_DESTINATION, response_code=~'5.*'}[1m]) ) by (source_app, destination_app)"
metricQuery_latency = "sum(irate(istio_request_duration_milliseconds_sum{reporter='source', MY_DESTINATION}[1m])) by (source_app, destination_app) / sum(irate(istio_request_duration_milliseconds_count{reporter='source', destination_app!='unknown', MY_DESTINATION}[1m])) by (source_app, destination_app)"
metricQuery_okHTTP = "sum(rate(istio_requests_total{reporter='source', response_code=~'2.*', MY_DESTINATION}[1m]) ) by (source_app, destination_app)"
metricQuery_PercentageCPUperPod = "sum(irate(container_cpu_user_seconds_total{id=~'/kubepods/burstable/.*'}[1m])) by (pod)"
metricQuery_ThrottlingCPUperPod = "sum((rate(container_cpu_cfs_throttled_periods_total[1m]) / rate(container_cpu_cfs_periods_total[1m])) * 100) by (pod)"