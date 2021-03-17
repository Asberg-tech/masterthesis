from datetime import datetime
from time import sleep
from savemetametrics import saveMetrics
import subprocess
import subprocess
import shlex


def manage_replica_count(deployList):
    print("\n********Begin test, change replica********")
    for i in range(0, len(deployList),1):
        # print(deployList[i])
        print("\n\tNew test:")
        print("Deployment: %s" % (deployList[i]) )
        # print("\t%s" % (deployList[i]))
        path = "./database/" + deployList[i] + ".xlsx"
        # print(path)
        
        #Scale up
        print("Scaling up deployment: %s" % deployList[i])
        subprocess.call(['./scale.sh', deployList[i], "2"])
        sleep(100)
        print("Saving metrics for: %s" % (deployList[i]))
        saveMetrics(path, deployList[i], "TwoReplica")
        sleep(10)
        
        #Scale down 
        print("Scaling down deployment: %s" % deployList[i])
        subprocess.call(['./scale.sh', deployList[i], "1"])
        sleep(20)
