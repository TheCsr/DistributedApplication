import numpy as np



def match_id(_id:np.array, keys: np.array):
    """
    This function computes the DOT product of the received ID to all the keys
    """
    similarity_vector = np.dot(keys, _id)
    highest_similarity = max(similarity_vector)
    best_key_idx = np.where( similarity_vector == highest_similarity)
    return keys[best_key_idx]


    
