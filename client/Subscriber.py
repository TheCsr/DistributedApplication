import sys
import json
import requests
import numpy as np
import random
import pandas as pd

from flask import Flask, request, Response, render_template
from Decrypt import DecryptMessage, NpEncoder
from Vector import Vector

CHUNK_SIZE = 1000
PADDING_SIZE = CHUNK_SIZE % 7
DATA_SIZE = CHUNK_SIZE - PADDING_SIZE

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8080



def main(argv): # Takes as arguments the publisher network information from terminal e.g python Publisher.py 127.0.0.1:5000

    client_args = argv[0].split(":") # ["127.0.0.1", "5000"]
    CLIENT_ADDRESS = client_args[0] # Address
    CLIENT_PORT = client_args[1] # Port number

    # We check saved ID associated to client IP address and PORT number
    file_name= "./templates/subscribers.csv"

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


    print(f"My SUBSCRIBER ID in string format is: {_id.to_string()}") 
    app = Flask(__name__) # Flask app



    # Render home page of publisher
    @app.route('/')
    def index():
        return render_template("subscriber.html", data="", _id=_id.to_string())


    # Subscribe to client's data to the server
    @app.route('/subscribe', methods=['GET'])
    def subscribe():
            url = f"http://{SERVER_ADDRESS}:{SERVER_PORT}/getData" # Define the server's URL + endpoint
            #target_id_string = request.form.get("target_id") # Get user input from GUI


            
            target_id_string = "1101111000000011011000001111101100000001000100101000101111010110001011111110101000011100100001010100010000010111100101110011110011001001000110100101111101010100100101011110100110011010011110101101001010110000010001011111101111001011111001011010001111100010000011011001001001011010100100011101101010110011000001110110100101101111111110101001100100000101110000000011010001000000011001001111010000000111111101001000000101110111000010010111101000001110011111100000111111111010000001101100000100011001001001111010111101100110000110101001010010111111011101111000110010100000000100011000000100010001010000001110100000100001001100000101010111100000101000111011110111110111001110000010000110010101111011110010001001011110001010001001101001100000101010001100110111010010011011101000000010101110110011011000110000111101010001111111100100110010100011101010010111111010100000001111111000100011101101001111000100110110111101101100100000110000100000010010101010111110101000110110010000000010111110100110011100001110"
            if target_id_string:
                # Handle the ID_ASCI values and transform it into a BIPOLAR vector! 
                target_id = Vector(binary_vector= np.array([int(b) for b in target_id_string]) ) # Transform ascii to binary then a Vector object
                response = requests.get(url, json = json.dumps(target_id.to_bipolar(), cls=NpEncoder)) # Post bipolar ID to server
                payload = json.loads(response.text)
                
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






