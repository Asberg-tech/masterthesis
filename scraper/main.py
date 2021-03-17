from findtop import top3_latency
from managereplica import manage_replica_count
from savemetametrics import saveMetrics
from datetime import datetime
import subprocess
import shlex


def main():
    
    #Get metrics when saturated
    # saveMetrics("saturatedMetrics.xlsx")
    saveMetrics("./database/" + "saturatedMetrics.xlsx", "", "noReplica")
    #Get top 3 latency edges
    topDeploys = top3_latency()
    manage_replica_count(topDeploys)
    # savemetrics()
    
if __name__ == '__main__':
    main()