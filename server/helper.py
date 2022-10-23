import numpy as np
import pymongo

#create connection with the mongodb
def create_connection(db_file):
    client = pymongo.MongoClient("mongodb+srv://thecsr:abcd1234@cluster0.spfiabd.mongodb.net/?retryWrites=true&w=majority")
    mydb = client[db_file]
    return mydb

# function to update the database document i.e in our case update the data list with new chunk
def update_tags(coll, entry_id, new_tag):
    coll.update_one({'entry_id': entry_id}, {'$push': {'data': new_tag}})


def compute_similarity(vector:np.array, keys:np.array) -> tuple:
    similarity_vector = list(np.dot(keys, vector)) # Compute similarity values with dot product
    for idx, val in enumerate(similarity_vector):
        print(f"Similarity value for entry {idx+1} is {val}")

    max_similarity = max(similarity_vector) # Get highest similarity value 
    idx = similarity_vector.index(max_similarity) # Get index (or entry number) of key with highest similarity
    #selected_key = keys[idx] # Retreive the key
    entry_id = idx+1
    return max_similarity, entry_id # Return (highest similarity, entry number, corresponding key)





