import sys
import json
import requests
import numpy as np
import pandas as pd
import random

from flask import Flask, request, Response, render_template
from Encrypt import EncryptMessage, NpEncoder
from Vector import Vector

CHUNK_SIZE = 1000
PADDING_SIZE = CHUNK_SIZE % 7
DATA_SIZE = CHUNK_SIZE - PADDING_SIZE

SERVER_ADDRESS = "13.48.104.200"
SERVER_PORT = 8081




def main(argv): # Takes as arguments the publisher network information from terminal e.g python Publisher.py 127.0.0.1:5000

    client_args = argv[0].split(":") # ["127.0.0.1", "5000"]
    CLIENT_ADDRESS = client_args[0] # Address
    CLIENT_PORT = client_args[1] # Port number

    # We check saved ID associated to client IP address and PORT number
    file_name= "./templates/publishers.csv"
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
        random_id = [ random.randint(0, 1) for i in range(DATA_SIZE)] + [1 for i in range(PADDING_SIZE)]
        _id = Vector(np.array(random_id)) # Generate vector ID
        row = pd.DataFrame([{"ip":CLIENT_ADDRESS, "port":CLIENT_PORT, "id": _id.to_string()}])
        df = pd.concat([df, row])
        df.to_csv(file_name, index=False)

    print(f"My PUBLISHER ID in string format is: {_id.to_ascii()}") 

    app = Flask(__name__) # Flask app


    # Render home page of publisher
    @app.route('/')
    def index():
        return render_template("publisher.html", data="", _id=_id.to_ascii())


    # Publish client's data to the server
    @app.route('/publish', methods=['POST'])
    def publish():
        url = f"http://{SERVER_ADDRESS}:{SERVER_PORT}/sendData" # Define the server's URL + endpoint
        message = request.form.get("message") # Get user input from GUI

        if message: # Check if message is empty
            msg = EncryptMessage(message = message , chunk_size = CHUNK_SIZE) # Instanciate the Message class
            encrypted_chunks = msg.encrypt(_id = _id.to_bipolar()) # Encrypt the message by embedding the ID

            for chunk in encrypted_chunks: # encrypted_chunks is a list of all encrypted chunks 
                response = requests.post(url, json = json.dumps(chunk, cls=NpEncoder)) # Post each chunk
                print(response.text) # Server replies back "Chunk received!"

            return render_template("publisher.html", data="Successful publish of message.", _id=_id.to_ascii())

        else:
            print("haha")
            return render_template("publisher.html", data="Write a message to send!", _id=_id.to_ascii())






    app.run(debug=True, host=CLIENT_ADDRESS, port=int(CLIENT_PORT))

if __name__ == "__main__":
    main(sys.argv[1:])


