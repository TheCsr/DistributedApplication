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


""" database initilization"""
db_name = "myDatabase"
mydb = create_connection(db_name)
COLLECTION_NAME = "PubSubData"


# Handle the received data from the client
@app.route('/sendData', methods=['POST'])
def save_data():
    collection = mydb[COLLECTION_NAME] # Get collection
    entries = [ doc for doc in collection.find()] # Retrieve all documents within the collection
    N = len(entries) # Number of entries in database == Number of total documents
    keys = [ entry["key"] for entry in entries] # Get keys from map table (list of lists)        

    chunk = json.loads(request.get_json()) # Chunk received from publisher
    if not N: # Check number of entries
        N += 1
        collection.insert_one({ "entry_id": N ,"key": chunk, "data": [chunk]})   #add the first entry to the database
    else:
        # Compute similarity chunk with respect to all keys in table
        max_similarity, entry_id = compute_similarity(vector=np.array(chunk), keys=np.array(keys))
        if max_similarity > THRESHOLD: # Check if similarity value is above threshold
            print(max_similarity)
            update_tags(collection, entry_id, chunk)  # Append chunk data to the key that gives highest similarity (max_sim_key)
        else:
            N += 1 # Increment number of entries in the table
            collection.insert_one({"entry_id": N ,"key": chunk, "data": [chunk]}) #creating a new document if max_sim < threashold

    # Print count of data chunks saved in db with respect to each entry
    collection = mydb[COLLECTION_NAME] # Get collection
    entries = [ doc for doc in collection.find()] # Retrieve all documents within the collection
    count_data = {entry["entry_id"]: len(entry["data"]) for entry in entries}
    print(count_data)

    return Response(response=json.dumps("Chunk received"), mimetype="application/json", status=200)


# Send messages to subscribers
@app.route('/getData', methods=['GET'])
def get_data():
    collection = mydb[COLLECTION_NAME] # Get collection
    entries = [ doc for doc in collection.find()] # Retrieve all documents within the collection
    N = len(entries) # Number of entries in database == Number of total documents

    if N:
        keys = [ entry["key"] for entry in entries] # Get keys from map table (list of lists)        
        bipolar_target_id = json.loads(request.get_json()) # Handle the received bipolar ID from client through the GET request
        print(f"There are {N} entries in the database.")
        # Compute similarity degree of DOT product between KEYS and Id
        print(f"Computing similarity for requested ID and map table keys: ")
        max_similarity, entry_id = compute_similarity(vector=np.array(bipolar_target_id), keys=np.array(keys))

        if max_similarity > THRESHOLD: # if ID corresponds to KEY
            my_query = {"entry_id": entry_id} # Query sent to database 
            target_entry = collection.find_one(my_query) # Find document which corresponds to entry with highest similarity
            print(f"The ID sent corresponds to entry {entry_id}") 
            messages = target_entry["data"] # From the entry selected, return the messages ("data" as key)
            print(f"The number of messages returned is: {len(messages)}")
            return Response(response=json.dumps({"messages": messages}), mimetype="application/json", status=200)

        else: # if ID does not correspond to any key
            return {"response": "Your id does not correspond to any key in database" }
    else:
        return {"response": "Data base is empty! Nothing to subscribe to!"}


    
    


if __name__ == "__main__":
    app.run(debug=True, host=SERVER_ADDRESS, port=SERVER_PORT)