import os
import json
import numpy as np
import requests
from flask import Flask
from flask import Response, request
from Encrypt import EncryptMessage, NpEncoder
from helper import generate_id

CHUNK_SIZE = 1001
CLIENT_ADDRESS = "127.0.0.1"
CLIENT_PORT = 5000

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8080

app = Flask(__name__)

client_id, client_id_ascii = generate_id(dimension=CHUNK_SIZE)



@app.route('/')
def index():
    pass


@app.route('/post', methods=['POST'])
def POST():
    """
    When this method is post method is triggered, it receives client's data input from the GUI
    """
    url = f"{SERVER_ADDRESS}:{SERVER_PORT}/sendData"
    msg = EncryptMessage(
        message = "Haha" ,
        chunk_size = CHUNK_SIZE
        )
    msg.encrypt(_id = client_id)    
    data = {'chunks': msg.encrypted_chunks}
    requests.post(url, json = json.dumps(data, cls=NpEncoder))

@app.route('/get', methods=['GET'])
def GET():
    url = f"{SERVER_ADDRESS}:{SERVER_PORT}/getData"
    _id = request.args.get('data')
    get_request = requests.get(url, params = {"Id": _id})
    response = get_request.text

    try:
        data = json.loads(response)
        a = json.loads(_id)
    except:
        return "REQUEST FAILED FOR SOME REASON"
    
    # print(response_list)

    id_refined = decoder.refine_id(json.loads(idList))
    # print(id_refined)



if __name__ == "__main__":
    app.run(debug=True, host=CLIENT_ADDRESS, port=CLIENT_PORT)


