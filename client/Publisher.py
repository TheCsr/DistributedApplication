import sys
import json
import requests
import numpy as np
import random

from flask import Flask, request, Response, render_template
from Encrypt import EncryptMessage, NpEncoder
from Vector import Vector

CHUNK_SIZE = 5

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8080



def main(argv): # Takes as arguments the publisher network information from terminal e.g python Publisher.py 127.0.0.1:5000

    client_args = argv[0].split(":") # ["127.0.0.1", "5000"]
    CLIENT_ADDRESS = client_args[0] # Address
    CLIENT_PORT = int(client_args[1]) # Port number
    _id = Vector(np.array([ random.randint(0, 1) for i in range(CHUNK_SIZE)])) # Generate vector ID
    print(f"My PUBLISHER ID in ASCII format is: {_id.to_ascii()}") 

    app = Flask(__name__) # Flask app


    # Render home page of publisher
    @app.route('/')
    def index():
        return render_template("index.html", data="", _id=_id.to_ascii())


    # Publish client's data to the server
    @app.route('/publish', methods=['POST'])
    def publish():
        url = f"http://{SERVER_ADDRESS}:{SERVER_PORT}/sendData" # Define the server's URL + endpoint
        message = request.form.get("message") # Get user input from GUI

        if message: # Check if message is empty
            msg = EncryptMessage(message = message , chunk_size = CHUNK_SIZE) # Instanciate the EncryptMessage class
            encrypted_chunks = msg.encrypt(_id = _id.to_bipolar()) # Encrypt the message by embedding the ID

            for index, chunk in enumerate(encrypted_chunks): # encrypted_chunks is a list of all encrypted chunks 
                data = (index, chunk)
                response = requests.post(url, json = json.dumps(data, cls=NpEncoder)) # Post each chunk
                print(response.text) # Server replies back "Chunk received!"

            return render_template("index.html", data="Successful publish of message.", _id=_id.to_ascii())

        else:
            return render_template("index.html", data="Write a message to send!", _id=_id.to_ascii())






    app.run(debug=True, host=CLIENT_ADDRESS, port=CLIENT_PORT)

if __name__ == "__main__":
    main(sys.argv[1:])


