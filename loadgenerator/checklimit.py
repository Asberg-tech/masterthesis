from prometheus_api_client import PrometheusConnect,  MetricSnapshotDataFrame, MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta
import pandas as pd
from datetime import timedelta


prom = PrometheusConnect(url ="http://localhost:9090", disable_ssl=True)


def check_errors():
    metric_data = prom.custom_query(query="sum(rate(istio_requests_total{reporter='source', response_code=~'5.*'}[2m]) ) by (source_app, destination_app)",
        )
    # To make it a table where each row is a metric
    metric_df = MetricSnapshotDataFrame(metric_data)

    #Convert value type to int
    metric_df[['value']] = metric_df[['value']].apply(pd.to_numeric)
    #Convert to clocktime
    metric_df[['timestamp']] = metric_df[['timestamp']].apply(pd.to_datetime,unit='s')

    error_df = metric_df.loc[(metric_df['value'] > 3)]
    
    ErrorExist = False
    if error_df.empty:
        print('\n***No errors occuring!***\n')
        return ErrorExist
    else:
        print("\n***Number of errors***\n")    
        print(error_df)
        ErrorExist = True
        return ErrorExist