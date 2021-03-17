from prometheus_api_client import PrometheusConnect,  MetricSnapshotDataFrame, MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta
import pandas as pd

from datetime import timedelta

def saveMetricsToFile (filepath, metrics, sheetName, column, row):
    writer = pd.ExcelWriter(filepath)
    metrics.to_excel(writer, index = False, sheet_name = sheetName, startrow=row, startcol=column )
    writer.save()

def queryMetrics(customquery, trim):
    # print("\n queryMetrics START\n")

    prom = PrometheusConnect(url ="http://localhost:9090", disable_ssl=True)

    data = prom.custom_query(query=customquery,
     )
    # To make it a table where each row is a metric
    df = MetricSnapshotDataFrame(data)
    df = df[df.value != "NaN"]

    df[['value']] = df[['value']].apply(pd.to_numeric)
    df[['timestamp']] = df[['timestamp']].apply(pd.to_datetime, unit='s')

    sortedDf = df.sort_values('value', ascending=False).head(trim)

    # print(nicenumbers)
    # print(df.index)
    # print(df.columns)
    # print("\n queryMetrics END\n")
    return sortedDf




