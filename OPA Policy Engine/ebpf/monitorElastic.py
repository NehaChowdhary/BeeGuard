#!/usr/bin/python3
# e.g. $ python monitorElastic.py -p 10

import time
import argparse
import requests
import sys
import os
from io import BytesIO
from datetime import datetime
import signal
import psutil
import subprocess
#############################################################################
# Elastic configuration
URL = os.environ.get('URL')
DOC_ID="data"
LAST_DATA_VERSION=None

#############################################################################
def kill_command(cmd):
    flag=[]
    print("_________________________")
    for proc in psutil.process_iter(['pid', 'name']):
        # Check whether the process name matches
        if cmd in proc.info['name']:
            pid=proc.info['pid']
            os.kill(pid, signal.SIGTERM)
            print("INFO: Killed "+str(pid))
            flag.append(pid)
    if(len(flag)>0):
        print("_________________________")
        return(flag)
    print("ERR: Kill Failed:"+cmd)
    print("_________________________")
    return(False)
#############################################################################
def execute_command(cmd):
    """Execute a command and return the exit status"""
    return os.system(cmd)
#############################################################################
def child_process(cmd):
    """Child process function"""
    while True:
        status = execute_command(cmd)
        if status == 0:
            break
        else:
            print("_________________________")
            print("ERR: Command Failed:"+cmd)
            print("ERR: retrying in 5 seconds...")
            print("_________________________")
            time.sleep(5)
#############################################################################
def parse_args():
    parser = argparse.ArgumentParser(description="Scheduler to check changes in elasticsearch")
    parser.add_argument('-p', '--periodicity',  default=1, type=int, dest='timePeriod', help='Script periodicity in seconds')
    args = parser.parse_args()
    return args
#############################################################################
def getDataVersion():
    # Specify the URL of the Elasticsearch server and document ID
    url = URL+'/_doc/'+DOC_ID
    response=None
    while True:
        try:
            response = requests.get(url)
            break
        except  requests.exceptions.ConnectionError:
            print("_________________________")
            print('ERR: Connection refused, waiting for 5 seconds before retrying...')
            print("_________________________")
            time.sleep(5)
    # Parse the JSON response
    data = response.json()
    if('error' in data.keys()):
        print("_________________________")
        print("ERR: Load data in elasticsearch")
        print("_________________________")
        return(None)
    # Extract and print the version
    version = data["_version"]

    return(version)
    #print("Version:", version)

#############################################################################
OPA_PID=None
args=parse_args()
print(args)
while True:
    currVersion=getDataVersion()
    if(currVersion==None):
        print("ERR: Unable to fetch data version")
    elif(currVersion != LAST_DATA_VERSION):
        # Fetch data script
        print("\nNeed to fetch data")
        LAST_DATA_VERSION=getDataVersion()
        print("Current Data version:"+ str(LAST_DATA_VERSION))
        print("##############")
        os.system("python3 extractFromCapabilityTree.py -d cumulativeCapabilities.json -e")
        print("##############")
        print("INFO: Restart OPA("+str(OPA_PID)+")")
        #ret=kill_command("/usr/local/bin/opa")
        ret=kill_command("opa")
        if(ret):
            print("INFO: Killed OPA")
        else:
            print("_________________________")
            print("ERR: Killing OPA failed!!")
            print("_________________________")
        print("------------------------------------------------")
        #child_process('/usr/local/bin/opa run --server --log-level debug /example')
        process = subprocess.Popen(['/usr/local/bin/opa', 'run', '--server', '--log-level', 'debug', '/example'])
        print("------------------------------------------------")
        #print('INFO: Child PID:'+str(OPA_PID))
    else:
        #sys.stdout.write(".")
        # Get current date and time
        now = datetime.now()
        # Format as string in your preferred format
        timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
        # Print log message with timestamp
        print(f'[{timestamp_str}] .')
    time.sleep(args.timePeriod)
