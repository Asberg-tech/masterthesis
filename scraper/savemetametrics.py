import pandas as pd
from metricshandler import queryMetrics, saveMetricsToFile

def saveMetrics(filepath, deployment, sheetName):
    #Top X 
    top3 = 3
    numberOfDeploys = 10
    latency = "sum(irate(istio_request_duration_milliseconds_sum{reporter='source'}[1m])) by (source_app, destination_app) / sum(irate(istio_request_duration_milliseconds_count{reporter='source'}[1m])) by (source_app, destination_app)"
    latency_metrics = queryMetrics(latency, numberOfDeploys)
    latency_metrics['Type'] = 'latency'

    errors = "sum(rate(istio_requests_total{reporter='source', response_code=~'5.*'}[1m]) ) by (source_app, destination_app)"
    error_metrics = queryMetrics(errors, numberOfDeploys)
    error_metrics['Type'] = 'error'


    OKResponseDeploy = "sum(rate(istio_requests_total{reporter='source', response_code=~'2.*'}[1m]) ) by (source_app, destination_app)"
    OKResponseDeploy_metrics = queryMetrics(OKResponseDeploy, numberOfDeploys)
    OKResponseDeploy_metrics['Type'] = 'OkResponseDeploy'

    percentageCPUperPod = "sum(irate(container_cpu_user_seconds_total{id=~'/kubepods/burstable/.*'}[1m])) by (pod)"
    percentageCPUperPod_metrics= queryMetrics(percentageCPUperPod, numberOfDeploys)
    percentageCPUperPod_metrics['Type'] = 'percentageCPUperPod'

    throttlingPerPod= "sum((rate(container_cpu_cfs_throttled_periods_total[1m]) / rate(container_cpu_cfs_periods_total[1m])) * 100) by (pod)"
    throttlingPerPod_mertics = queryMetrics(throttlingPerPod, numberOfDeploys)
    throttlingPerPod_mertics['Type'] = 'throttlingPerPod'

    combined_metrics = error_metrics.append(latency_metrics) 
    combined_metrics = combined_metrics.append(OKResponseDeploy_metrics) 
    combined_metrics = combined_metrics.append(percentageCPUperPod_metrics) 
    combined_metrics = combined_metrics.append(throttlingPerPod_mertics)
    # if deployment: 
    #     combined_metrics["Service"] = deployment


    # print(combined_metrics)
    saveMetricsToFile(filepath, combined_metrics, sheetName, 0 , 0)
    # saveMetricsToFile(error_metrics,'NoReplica1', 0 , 5)

    # pd.concat([error_metrics.reset_index(), latency_metrics], axis=1)

