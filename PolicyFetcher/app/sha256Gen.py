#!/usr/bin/python3
# e.g. $ python3 sha256Gen.py
#############################################################################
from flask import Flask, request
import hashlib
import locallib
#############################################################################
app = Flask(__name__)
#############################################################################
def update_kvstore(fileHash):
    if(locallib.search_key(fileHash,locallib.FILENAME)):
        print("Entry exists:"+fileHash)
    else:
        entry={fileHash:-1}
        locallib.push_decisions(kvUpdate=entry)
#############################################################################
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    #D = read_request(request)
    #app.logger.info("Info: "+ type(D))
    if not request.data:
        print("Header only request")
        data["msg"]="Header only"
        return(jsonify(data))
    if 'file' not in request.files:
        data["msg"]="No File"
        D=request.data.decode('utf-8') if request.data else None
        data["hashStream"]=getSHA256(D)
        update_kvstore(data["hashStream"])
        return(jsonify(data))
    else:
        file = request.files['file']
        file_data = file.read()
        data["fileHash"]=getSHA256(file_data)
        update_kvstore(data["fileHash"])
    return(jsonify(data))
#############################################################################
def getSHA256(data):
    dt=hashlib.sha256(data.encode('utf-8')).hexdigest()
    return(dt)
#############################################################################
if __name__ == '__main__':
    locallib.initilizer()
    app.run(host='0.0.0.0', port=5000)
