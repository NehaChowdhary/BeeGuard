import requests
import json
import os
import time
import csv
import shutil
#############################################################################
# Configuration
# Set the environment variables
os.environ['OPA_BUNDLE_ID'] = "bundles/HXD3nbpalc"
os.environ['FILENAME'] = '/boot/kvstore'
os.environ['URL'] = 'http://10.5.20.125:8181/v1/data/ebpf/allow'
# Access the environment variables
FILENAME = os.environ.get('FILENAME')
URL = os.environ.get('URL')
OPA_BUNDLE_ID = os.environ.get('OPA_BUNDLE_ID')
# Check if the variables are properly set
print(f"FILENAME: {FILENAME}")
print(f"URL: {URL}")
print(f"OPA_BUNDLE_ID: {OPA_BUNDLE_ID}")

HEADERS = {'Content-Type': 'application/json'}
#############################################################################
# Read the string from /boot/bytecode.txt
with open('/boot/bytecode.txt', 'r') as file:
    data = file.read()

# Define the width of each element
element_width = 5

# Split the string into elements of width 5
elements = [data[i:i+element_width] for i in range(0, len(data), element_width)]

# Count the elements
count = len(elements)

# Typecast the elements from string to integer and calculate the sum
elements_as_int = [int(element) for element in elements]
sum_elements = sum(elements_as_int)

# Append the count to the sum to get the checksum
key = int(str(count) + str(sum_elements))
print("Key:", key)

#############################################################################
def initilizer():
    if(os.path.exists(FILENAME)):
        print(FILENAME + " exists")
        pass
    else:
        print(FILENAME + " does not exist")
        # source_file = "/app/dummy_kvstore.txt"
        # shutil.copy(source_file, FILENAME)
#############################################################################
def search_key(key,fname=FILENAME):
    with open(fname, 'r') as f:
        for line in f:
            k, v = line.strip().split()
            if(key == k):
                print("Key found in", FILENAME)
                return(True)
    return(False)
#############################################################################
def find_keys(fname=FILENAME):
    data=[]
    with open(fname, 'r') as f:
        for line in f:
            key, value = line.strip().split()
            if(int(value)<0):
                data.append(key)
    return(data)
#############################################################################
def push_decisions(kvUpdate={}):
    data = {}
    with open(FILENAME, 'r') as f:
        for line in f:
            key, value = line.strip().split()
            data[key] = value
    for k in kvUpdate.keys():
        data[k] = kvUpdate[k]
    # Write the updated key-value pairs back to the file
    with open(FILENAME, 'w') as f:
        for key, value in data.items():
            f.write(f'{key} {value}\n')
    return()
#############################################################################
def send_OPA_query(d):
    '''
    - False:curl --location 'http://localhost:8181/v1/data/ebpf/allow' --header 'Content-Type: application/json' --data '{"input": {"funcName": "mptm_decap"}}'
    - True:curl --location 'http://localhost:8181/v1/data/ebpf/allow' --header 'Content-Type: application/json'  --data '{"input": {"funcName": "mptm_encap"}}'
    '''
    data = {"input": {"signature": d}}
    response = requests.post(URL, headers=HEADERS, data=json.dumps(data))
    #print(response)
    decision=json.loads(response.text)
    #print(decision)
    if(decision['result']):
        return(1)
    else:
        return(0)
#############################################################################
def execute_update():
    data=find_keys(FILENAME)
    if(data != []):
        print("Update Values:"+json.dumps(data))
    kvUpdate={}
    for d in data:
        ret=send_OPA_query(d)
        print(d+" "+str(ret))
        kvUpdate[d]=str(ret)
    push_decisions(kvUpdate)
#############################################################################
def update_kvstore(fileHash):
    initilizer()
    execute_update()
    if(search_key(fileHash,FILENAME)):
        print("Entry exists:"+fileHash)
    else:
        entry={fileHash:-1}
        push_decisions(kvUpdate=entry)
#############################################################################
update_kvstore(key)
