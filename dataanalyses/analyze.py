from servicehandler import get_service_filename
from servicehandler import get_df_from_file 
from algorithm import algo_controller

    
def analyzer():
    #Get saturated metrics
    saturatedMetrics = get_df_from_file("saturatedMetrics.xlsx", "noReplica")

    servicesToAnalyze = get_service_filename()

    print("\n***Algorithm***")
    algo_controller(servicesToAnalyze[0], saturatedMetrics)

    # for service in servicesToAnalyze:
        # algo(service, saturatedMetrics)