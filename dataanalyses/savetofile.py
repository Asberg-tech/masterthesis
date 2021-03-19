from myconfig import *
import re

def clear_file():
    open('metricstoscalewith.txt', 'w').close()

def save_metrics_to_file(service, value, typeMetric):
    if (typeMetric == "error"):
        query = split_metric_string(service, metricQuery_okHTTP)
        f = open("metricstoscalewith.txt", "a")
        f.write("\nNew Metric!")
        f.write("\n*****Scale: %s if traffic exceed:     %s http per s******" % (service, value))
        f.write("\nMetrics: ")
        f.write(query)    
        f.close()        
    elif (typeMetric == "latency"):
        query = split_metric_string(service, metricQuery_latency)
        f = open("metricstoscalewith.txt", "a")
        f.write("\nNew Metric!")
        f.write("\n*****Scale: %s if latency exceed:     %s ms*****" % (service, value))
        f.write("\nMetrics: ")
        f.write(query)    
        f.close()

def split_metric_string(service, query):
    print("\nSplitting strings")
    replacement = "destination_app=" + "'" +  service + "'"
    result = re.sub(r"MY_DESTINATION", replacement, query)
    return result
