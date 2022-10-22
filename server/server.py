import os
import json
import numpy as np
from flask import Flask, request, render_template, Response
from Vector import Vector
import pymongo

from helper import *

app = Flask(__name__)

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8080
THRESHOLD = 10


global map_table



map_table = []

def create_connection(db_file):
    client = pymongo.MongoClient("mongodb+srv://thecsr:abcd1234@cluster0.spfiabd.mongodb.net/?retryWrites=true&w=majority")
    mydb = client[db_file]
    return mydb

def update_tags(coll, id, new_tag):
    coll.update_one({'ids': id}, {'$push': {'data': new_tag}})


@app.route('/sendData', methods=['POST'])
def save_data():
    """
        Handle the received data from the client
        Check if table is empty
        GET all keys
    """
    """ database initilization"""
    database = "myDatabase"
    mydb = create_connection(database)
    
    mycol = mydb["myCollection"]
    
    N = len(map_table) # Number of entries
    chunk = json.loads(request.get_json())
    
    if not N: # Check number of entries
        N += 1
        map_table.append({ "ids": N-1 ,"key": chunk, "data": [chunk]}) # Add the first entry of the 
        mycol.insert_one({ "ids": N-1 ,"key": chunk, "data": [chunk]})

    else:
        entries = map_table # Get entries e.g entry = {1: {"key": [list], "data": [[list of lists]] }}
        keys = [ entry["key"] for entry in entries] # Get keys from map table (list of lists)

        # Compute similarity chunk with respect to all keys in table
        max_sim, max_sim_key, max_sim_entry = maximum_similarity(chunk=np.array(chunk), keys= np.array(keys))

        if max_sim > THRESHOLD: # Check if max_sim value is above threshold
            map_table[max_sim_entry-1]["data"].append(chunk) # Append chunk data to the key that gives highest similarity (max_sim_key)
            update_tags(mycol, int(max_sim_entry-1), chunk )
            
        else:
            N += 1 # Increment number of entries in the table
            map_table.append({"ids": N-1 ,"key": chunk, "data": [chunk]}) # Create a new entry with the new chunk as a key
            mycol.insert_one({"ids": N-1 ,"key": chunk, "data": [chunk]})

        
    
    # count_data = {k: len(v["data"]) for (k, v) in map_table}
    count_data = {map_table.index(item): len(item["data"]) for item in map_table}
    print(count_data)
    print(map_table)

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
    _id_ascii = json.loads(request.get_json())
    print(_id_ascii)
    


if __name__ == "__main__":
    app.run(debug=True, host=SERVER_ADDRESS, port=SERVER_PORT)