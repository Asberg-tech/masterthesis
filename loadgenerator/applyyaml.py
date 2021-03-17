import subprocess
from datetime import datetime

def apply_yaml():
    print("start: %s" % (datetime.now()))
    rc = subprocess.call("./updatedeploy.sh")

    print("end: %s" % (datetime.now()))
