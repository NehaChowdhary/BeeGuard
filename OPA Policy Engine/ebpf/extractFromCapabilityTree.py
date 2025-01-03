#!/usr/bin/python3

# e.g. $ python extractFromCapabilityTree.py -s ../input_store/xdp-mptm-main_annotated_formatted.db -d cumulativeCapabilities.json
import json
import argparse
import inquirer
import pycurl
import os
from io import BytesIO
#############################################################################
# Elastic configuration
URL = os.environ.get('URL')+'/type'
DOC_ID="data"
#############################################################################
def parse_args():
    parser = argparse.ArgumentParser(description="Convert Persona JSON to OPA compatible JSON")
    parser.add_argument('-s', '--source',nargs='*', dest='input_file', help='Input filenames. Multiple filenames results a merged output.',required=False)
    parser.add_argument('-d', '--destination', dest='output_file', help='Output filename',required=False)
    parser.add_argument('-e', '--no-config', dest='inq', action='store_true', help='no enquiry to help automatic execution')
    args = parser.parse_args()
    return args
#############################################################################
def DFS(node_idx,data):
    # Terminate if Leaf node
    #print(node_idx,data[node_idx]["funcName"])
    functions_called_index=[]
    if(len(data[node_idx]["called_function_list"])==0):
        functions_called_index.append(node_idx)
        return(functions_called_index)
    else:
        for fname in data[node_idx]["called_function_list"]:
            childNode_idx=[d for d in list(data.keys()) if (data[d]["funcName"]==fname)]
            functions_called_index=functions_called_index + DFS(childNode_idx[0],data)
            #print(node_idx,functions_called_index)
        return(functions_called_index)
#############################################################################
def getCumulativeCapabilities(data):
    newdata=data
    for i in list(data.keys()):
        nodeList= DFS(i,data)
        funcNameList=[data[n]["funcName"] for n in nodeList]
        data[i]["cumulative_called_function_list"]=funcNameList
        data[i]["cumulative_capabilities"]=[capabilities["capability"] for n in nodeList+[i] for capabilities in data[n]["capabilities"]]
    while True:
        for i in list(data.keys()):
            funcNameList=data[i]["cumulative_called_function_list"]
            nodeList= [f for f in data.keys() if(data[f]["funcName"] in funcNameList)]
            cumulative_capabilities = [capability for n in nodeList+[i] for capability in data[n]["cumulative_capabilities"]]
            data[i]["cumulative_capabilities"]=list(set(cumulative_capabilities))
            #print(data["_default"][i]["called_function_list"])
        if(data==newdata):
            return(data)
        else:
            print("New Iteration")
#############################################################################
def filterFields(data,keep=[]):
    if(len(keep)==0):
        pass
    else:
        for PID in data:
            D=data[PID]
            for field in list(D.keys()):
                if field in keep:
                    pass
                else:
                    D.pop(field, None)
            data[PID]=D
    return(data)
#############################################################################
def getKeepFileds(d,keep=[]):
    # Define a list of choices
    options = list(d[list(d.keys())[0]].keys())+['cumulative_capabilities',"cumulative_called_function_list"]
    # Create a prompt for the user to select a choice
    question = [
        inquirer.Checkbox('fields',
                      message='Select important fields (Do not turn-off the defaults):',
                      choices=options,
                      default=keep)
    ]
    # Get user input
    if(args.inq):
        return(keep)
    else:
        answers = inquirer.prompt(question)
    #print('Selected fields:')
    #for f in answers['fields']:
    #    print("\t"+f)
    return(answers['fields'])
#############################################################################
def fetch(dID):
    url = URL+'/'+dID
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION, buffer.write)
    c.perform()
    # Get the response from the Elasticsearch server
    response = buffer.getvalue()
    c.close()
    return(response)
#############################################################################
def mergeFunctions(d,sign):
    keys=set(k for k in d.keys() if d[k]['signature']==sign)
    if(len(keys)==0):
        return(d)
    else:
        ND={"signature":sign}
        newKey= "+".join(keys)
        k=list(keys)[0]
        listTypeCapability=[cap for cap in d[k].keys() if isinstance(d[k][cap], list)]
        for lcap in listTypeCapability:
            temp=[d[k][lcap] for k in keys ]
            temp=list(set([element for sublist in temp for element in sublist]))
            ND[lcap]= temp
        strTypeCapability=[cap for cap in d[k].keys() if isinstance(d[k][cap], str)]
        for scap in strTypeCapability:
            temp=[d[k][scap] for k in keys ]
            #temp=list(set([element for sublist in temp for element in sublist]))
            ND[scap]= temp
        # delete old entries from d
        d = {key: value for key, value in d.items() if key not in keys}
        # add new entry 
        d[newKey]=ND
    return d
#############################################################################
def process_file(data):
    keep=getKeepFileds(data["_default"],keep=['funcName','signature','personaFileName', 'cumulative_capabilities',"cumulative_called_function_list"])
    newdata={"_default":getCumulativeCapabilities(data["_default"])}
    newdata={"_default":filterFields(newdata["_default"],keep=keep)}
    print("******************************************************************************************")
    print("Merge functions with same signature")
    try:
        signatureSet=set(newdata["_default"][k]['signature'] for k in newdata["_default"].keys())
        for sign in list(signatureSet):
            newdata["_default"]=mergeFunctions(newdata["_default"],sign)
    except:
        print("signatureSet")
    print("******************************************************************************************")
    print("Replace ProgramID with signature")
    newdata["_default"] = {v["signature"]: v for v in newdata["_default"].values()}
    print("******************************************************************************************")
    return(newdata)
#############################################################################
''' Ipython Stub
parser = argparse.ArgumentParser(description="Convert Persona JSON to OPA compatible JSON")
args = parser.parse_args()
args.input_file=["../input_store/xdp-mptm-main_annotated_formatted.db"]
args.output_file="cumulativeCapabilities.json"
fieldName="funcName"
for key in data["_default"].keys():
    print(key,data["_default"][key][fieldName])
'''
#############################################################################
### Main code starts from here
args=parse_args()
outputdata={"_default":{}}
if(args.input_file == None):
    #Fetch from Elastic Server
    response=fetch(DOC_ID)
    fetched=json.loads(response)
    data=fetched['_source']
else:
    for f in args.input_file:
        data=json.load(open(f))
        print("******************************************************************************************")
        print("***  Processing file "+f+"  ***")
        # Add personaFileName for each entry 
        for key, value in data['_default'].items():
            value["personaFileName"] = f
        outputdata['_default'].update(process_file(data)["_default"])
if(args.output_file == None):
    # Store in local temp file
    with open("temp.json", 'w') as file:
        json.dump(outputdata, file,indent = 4, ensure_ascii = True)
    print("Stored data in file: temp.json")
else:    
    with open(args.output_file, 'w') as file:
        json.dump(outputdata, file,indent = 4, ensure_ascii = True)
    print("Stored data in file: "+args.output_file)
print("******************************************************************************************")