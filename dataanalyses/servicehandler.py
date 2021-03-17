import os
import pandas as pd
 
def get_service_filename(): 
    arr = os.listdir('../scraper/database')
    lst = []
    for service in arr:
        if not "saturatedMe" in service:
            lst.append(service)
    print("Servicelist to analyze:  %s" % (lst))
    return lst

def get_df_from_file(filename, sheetName):
    print("\nRetreiving filename from:    %s" % (filename))
    filepath = '../scraper/database/' + filename
    df = pd.read_excel(
     filepath,
     engine='openpyxl',
     sheet_name=sheetName
    )
    return df