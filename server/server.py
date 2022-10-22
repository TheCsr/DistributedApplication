import os
import json
import numpy as np
from flask import Flask, request, render_template, Response
from Vector import Vector

from helper import *

app = Flask(__name__)

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8080
THRESHOLD = 10


global map_table

map_table = {}



@app.route('/sendData', methods=['POST'])
def save_data():
    """
        Handle the received data from the client
        Check if table is empty
        GET all keys
    """
    N = len(map_table.keys()) # Number of entries
    chunk = json.loads(request.get_json())
    
    if not N: # Check number of entries
        N += 1
        map_table[N] = {"key": chunk, "data": [chunk]} # Add the first entry of the table

    else:
        entries = map_table.values() # Get entries e.g entry = {1: {"key": [list], "data": [[list of lists]] }}
        keys = [ entry["key"] for entry in entries] # Get keys from map table (list of lists)

        # Compute similarity chunk with respect to all keys in table
        max_sim, max_sim_key, max_sim_entry = maximum_similarity(chunk=np.array(chunk), keys= np.array(keys))

        if max_sim > THRESHOLD: # Check if max_sim value is above threshold
            map_table[max_sim_entry]["data"].append(chunk) # Append chunk data to the key that gives highest similarity (max_sim_key)
        else:
            N += 1 # Increment number of entries in the table
            map_table[N] = {"key": chunk, "data": [chunk]} # Create a new entry with the new chunk as a key

        print(max_sim)
    
    count_data = {k: len(v["data"]) for (k, v) in map_table.items()}
    print(count_data)

    return Response(response=json.dumps("Chunk received"), mimetype="application/json", status=200)


@app.route('/getData', methods=['GET'])
def get_data():
    """
        Check if data base is empty or not
        Retrieve all registered keys
        Handle the received ascii ID from client through the GET request
        Trasnform ASCII Id into a bipolar vector
        Compute similarity degree of DOT product between KEYS and Id
        Select KEY with highest value
        Retrieve data from database using KEY
        return data chunks to the client
    """
    
    pass


if __name__ == "__main__":
    app.run(debug=True, host=SERVER_ADDRESS, port=SERVER_PORT)