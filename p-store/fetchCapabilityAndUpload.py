#!/usr/bin/python3
## e.g. $ python3 fetchCapabilityAndUpload.py -f ../Opa-Engine/input_store/xdp-mptm-main_annotated_formatted.db -v
import json
import argparse
import pycurl
from io import BytesIO
from termcolor import colored, cprint
#############################################################################
URL = 'http://localhost:9200/index/type'
DOC_ID="data"
#############################################################################
def parse_args():
    parser = argparse.ArgumentParser(description="Upload capability JSON generated from CodeAnalyzer to Elastic")
    parser.add_argument('-f', '--file', dest='input_file', help='Input filename', required=True)
    parser.add_argument('-p', '--post', dest='post', help='View POST request', action='store_true')
    parser.add_argument('-g', '--get', dest='get', help='Do not see GET request', action='store_true')
    parser.add_argument('-v', '--validate', dest='validate', help='Validate with the source data', action='store_true')
    args = parser.parse_args()
    return args
#############################################################################
def pushToElastic(data,dID=""):
	url= URL+"/"+args.input_file if(len(dID) == 0) else URL+"/"+dID
	json_data = json.dumps(data)
	buffer = BytesIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, json_data)
	c.setopt(pycurl.WRITEFUNCTION, buffer.write)
	c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
	if(args.post):
		c.setopt(pycurl.VERBOSE, 1)
	c.perform()
	# Get the response from the Elasticsearch server
	response = buffer.getvalue()
	return(response.decode('UTF-8'))
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
''' Ipython Stub
parser = argparse.ArgumentParser(description="Stub")
args = parser.parse_args()
args.input_file="../Opa-Engine/input_store/xdp-mptm-main_annotated.db"
args.post=True
args.validate=True
'''
#############################################################################
args=parse_args()
data=json.load(open(args.input_file))
blank={}
response=pushToElastic(blank,dID=DOC_ID)
response=pushToElastic(data,dID=DOC_ID)
if(args.post):
	print(response)
	print("******************************************************************************************")
if(args.get or args.validate):
	response=fetch(DOC_ID)
if(args.get):
	print(response)
	print("******************************************************************************************")
if(args.validate):
	fetched=json.loads(response)
	if(fetched['_source']==data):
		print("Validation successfull!!")
	else:
		cprint("Validation unsuccessfull!!", "red", attrs=["bold"])