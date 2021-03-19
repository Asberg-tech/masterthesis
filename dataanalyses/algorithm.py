import os
import numpy as np
import pandas as pd

from myconfig import *
from savetofile import save_metrics_to_file
from servicehandler import get_df_from_file

def algo_controller(filenameService, saturatedMetrics):

    maxLatency = 800

    #Get df for service when scaled
    print("Filename:    %s" %(filenameService))
    service = os.path.splitext(filenameService)[0]
    print("\nService to analyze: %s\n" % service)
    #Get DF for service
    df = get_df_from_file(filenameService, "TwoReplica")

    #Retreive error data
    sortedSatError = filter_metric("error", saturatedMetrics)
    sortedError = filter_metric("error", df)
    sortedErrorByValue = sort_values(sortedSatError, sortedError)

    #Figure out if data number decrease when increased replica
    sortedErrorByValue["Decrease"] = np.where(sortedErrorByValue['value'] < sortedErrorByValue['SatValue'], 'True', 'False')
    sortedErrorByValue["Difference"] = np.where(sortedErrorByValue['value'] < sortedErrorByValue['SatValue'], sortedErrorByValue['value'] - sortedErrorByValue['SatValue'], 0 )

    
    #Retreive latency data
    sortedSatLatency = filter_metric("latency", saturatedMetrics)
    sortedLatency = filter_metric("latency", df)
    sorted_latency = sort_values(sortedSatLatency, sortedLatency)

    #Figure out if data number decrease when increased replica
    sorted_latency["Decrease"] = np.where(sorted_latency['value'] < sorted_latency['SatValue'], 'True', 'False')
    sorted_latency["Difference"] = np.where(sorted_latency['value'] < sorted_latency['SatValue'], sorted_latency['value'] - sorted_latency['SatValue'], 0 )
    
    print("Sorted combined df: ")
    print(sorted_latency)


    if latency_algo(sorted_latency, service):
        errorValue = error_algo(sortedErrorByValue, saturatedMetrics, service)
        if (errorValue != 0):
            print("\n*****Scale: %s if traffic exceed:     %s http per s******" % (service, errorValue))
            print("Metrics: " )
            print(metricQuery_okHTTP)
            save_metrics_to_file(service, errorValue, "error")
        else:
            print("\n*****Scale: %s if latency exceed:     %s ms*****" % (service, maxLatency))
            print("Metrics: " )
            print(metricQuery_latency)
            save_metrics_to_file(service, maxLatency, "latency")
   

def latency_algo(df, service):
    minDifferenceLatency = -500
    isolatedDF = df.loc[(df['destination_app'] == service) & (df['Difference'] <(minDifferenceLatency))]
    if isolatedDF.empty:
        print('DataFrame is empty!')
        return False
    else:
        print("\n***Latency decreases for service:  %s***" % (service))
        print(isolatedDF)
        return True
    

def error_algo(errorDF, satDF, service):
    minDifferenceError = -10
    percent = 0.9
    value = 0
    dfHTTP = filter_metric("OkResponseDeploy", satDF)
    print("errorDF")
    print(errorDF)
    print("DFHTTP")
    print(dfHTTP)
    isolatedHTTPDF = dfHTTP.loc[dfHTTP['destination_app'] == service]

    #If error decrease is bigger than 10
    isolatedDF = errorDF.loc[(errorDF['Decrease'] == "True") & (errorDF['Difference'] <(minDifferenceError))]

    if isolatedDF.empty:
        print('DataFrame is empty!')
        return False
    else:
        print("\n***Scale on Errors***")
        print("\nErrors")
        print(isolatedDF)
        print("\nHTTP request per s to service:   %s" %(service))
        print("Dataframe: ")
        print(isolatedHTTPDF)
        for i, row in isolatedHTTPDF.iterrows():
            if (value < row['value']):
                value = row['value']
        value = round(value * percent)
        return value

    # print(sort_values(errorDF, dfHTTP))





def filter_metric(typeMetric, df):
    metric = df.loc[df['Type'] == typeMetric]
    sortedMetric = metric.sort_values(['source_app', 'destination_app'])
    return pd.DataFrame(sortedMetric, columns= ['destination_app', 'source_app' , 'value'])





def sort_values(sortedSat, sorted):
    sortedSat.index = pd.RangeIndex(len(sortedSat.index))
    sorted.index = pd.RangeIndex(len(sorted.index))

    if (len(sortedSat.index) > len(sorted.index)):
        print("sortedSat is bigger than sorted: sorted.index:    %s sorted.index:    %s" % (len(sortedSat.index), len(sorted.index)))
        bigDF = sortedSat
        smallDF = sorted
    else:
        bigDF = sorted
        smallDF = sortedSat

    values = ["0"] * len(bigDF.index)
    for i, row in bigDF.iterrows():
        for j, row2 in smallDF.iterrows():
            if ((row['source_app'] == row2['source_app']) and (row['destination_app'] == row2['destination_app'])):
                values[i] = row2['value']

    bigDF["SatValue"] = values
    bigDF[["SatValue"]] = bigDF[["SatValue"]].apply(pd.to_numeric)
    bigDF[["value"]] = bigDF[["value"]].apply(pd.to_numeric)
    return bigDF

def convert_int(df, column ):
     df[[column]] = df[[column]].apply(pd.to_numeric)