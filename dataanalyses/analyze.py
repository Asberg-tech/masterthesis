from servicehandler import get_service_filename
from servicehandler import get_df_from_file 
from algorithm import algo_controller
from savetofile import clear_file


    
def analyzer():
    #clear output file
    clear_file()
    #Get saturated metrics
    saturatedMetrics = get_df_from_file("saturatedMetrics.xlsx", "noReplica")

    servicesToAnalyze = get_service_filename()

    print("\n***Algorithm***")
    # algo_controller(servicesToAnalyze[2], saturatedMetrics)

    for service in servicesToAnalyze:
        algo_controller(service, saturatedMetrics)