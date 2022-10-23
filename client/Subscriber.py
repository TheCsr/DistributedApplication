import sys
import json
import requests
import numpy as np
import random
import pandas as pd
import csv

from flask import Flask, request, Response, render_template
from Decrypt import DecryptMessage, NpEncoder
from Vector import Vector

CHUNK_SIZE = 1000
PADDING_SIZE = CHUNK_SIZE % 7
DATA_SIZE = CHUNK_SIZE - PADDING_SIZE

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8080
globalList = []
bsda="Hello"

def createListofCsv():
    with open('/home/thecsr/GENIAL/Mini Project/DistributedApplication/client/templates/publishers.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        list=[]
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                list.append(row[2])
                line_count += 1
        return list


def main(argv): # Takes as arguments the publisher network information from terminal e.g python Publisher.py 127.0.0.1:5000

    client_args = argv[0].split(":") # ["127.0.0.1", "5000"]
    CLIENT_ADDRESS = client_args[0] # Address
    CLIENT_PORT = client_args[1] # Port number

    # We check saved ID associated to client IP address and PORT number
    file_name= "./templates/subscribers.csv"
    listOfDropdown = createListofCsv()
    globalList = listOfDropdown


    df = pd.read_csv(file_name, header=0, dtype=str) # Read df csv file
    condition = (df['ip'] == CLIENT_ADDRESS) & (df['port'] == CLIENT_PORT) # Check if port & ip already exist in csv file
    bool_val = condition.any() 

    # No need to generate new ID
    if bool_val: 
        saved_str_id = df[condition].iloc[0]["id"] # Assign existing ID to client! 
        saved_binary_id = [int(c) for c in saved_str_id]
        _id = Vector(binary_vector= np.array(saved_binary_id)) # Generate vector ID

    # New IP/port generate a new ID        
    else: 

        data_bits = CHUNK_SIZE % 7
        random_id = [ random.randint(0, 1) for i in range(CHUNK_SIZE - data_bits)] + [1 for i in range(data_bits)]

        _id = Vector(np.array(random_id)) # Generate vector ID
        row = pd.DataFrame([{"ip":CLIENT_ADDRESS, "port":CLIENT_PORT, "id": _id.to_string()}])
        df = pd.concat([df, row])
        df.to_csv(file_name, index=False)


    # print(f"My SUBSCRIBER ID in string format is: {_id.to_string()}") 
    app = Flask(__name__) # Flask app


    # Render home page of publisher
    @app.route('/')
    def index():
        return render_template("subscriber.html", data="", _id=_id.to_string(), listOfList = globalList)


    # Subscribe to client's data to the server
    @app.route('/subscribe', methods=['POST'])
    def subscribe():
            url = f"http://{SERVER_ADDRESS}:{SERVER_PORT}/getData" # Define the server's URL + endpoint
            target_id_string = request.form.get("compSelect") # Get user input from GUI
            
            
            # target_id_string = "0001010011111111100000111111011011100111000110011000101000010100011010111011000000011000111011001001101000110011110000010100111110010011001111110010000001010011111101011000110000111100111001110000011000101001011000010111101110010100001011010111110101100100101110010000000110011100111000001111100010100010101100010010001010001001111010010101100110001101001110010101110011110100111000110010011101110011100111011100000110100100001101000101001111011101011000010101111001010100000101010100110000100001101111111110011110100000100001101110000010010100000111011001110011111111011010011100101110101010011101000110111111100011110000000001010011001101010110111101000011001111011110100011110000010100001111101010011111110000101100111000100111101010101110101100100101011010110100001000000101101101001000001011000010001001000101100100010011101100001101110101010011100001000010000101011111111001101011011000011111100101000100011110001000110000011000100101011100011011010001000101100001000111111110100100100011111111"
            if target_id_string:
                # Handle the ID_ASCI values and transform it into a BIPOLAR vector! 
                target_id = Vector(binary_vector= np.array([int(b) for b in target_id_string]) ) # Transform ascii to binary then a Vector object
                response = requests.get(url, json = json.dumps(target_id.to_bipolar(), cls=NpEncoder)) # Post bipolar ID to server
                payload = json.loads(response.text)
                print("payload", payload)
                bsda="asdasd"
                
                if "messages" in payload:
                    msg = DecryptMessage(encrypted_chunks=payload["messages"], chunk_size=CHUNK_SIZE)
                    decrypted_messages = msg.decrypt(_id=target_id.to_bipolar())
                    return render_template("subscriber.html", data=decrypted_messages, _id=_id.to_string())
                else:
                    return render_template("subscriber.html", data="Nothing to return", _id=_id.to_string())

    app.run(debug=True, host=CLIENT_ADDRESS, port=int(CLIENT_PORT))



if __name__ == "__main__":
    main(sys.argv[1:])

"""
if message: # Check if message is empty
    msg = Message(message = message , chunk_size = CHUNK_SIZE) # Instanciate the Message class
    encrypted_chunks = msg.encrypt(_id = _id.to_bipolar()) # Encrypt the message by embedding the ID

    for chunk in encrypted_chunks: # encrypted_chunks is a list of all encrypted chunks 
        response = requests.post(url, json = json.dumps(chunk, cls=NpEncoder)) # Post each chunk
        print(response.text) # Server replies back "Chunk received!"

    return render_template("publisher.html", data="Successful publish of message.", _id=_id.to_ascii())

else:
    return render_template("publisher.html", data="Write a message to send!", _id=_id.to_ascii())
"""






