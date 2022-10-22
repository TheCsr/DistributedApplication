import numpy as np



def match_chunk_to_key(chunk:np.array, keys: np.array, threshold:float):
    """
    This function computes the DOT product of the received ID to all the keys
    """
    similarity_vector = np.dot(keys, _id)
    highest_similarity = max(similarity_vector)
    best_key_idx = np.where( similarity_vector == highest_similarity)
    best_key = keys[best_key_idx]
    return best_key


def match_id_to_key(_id:np.array, keys: np.array):
    """
    This function computes the DOT product of the received ID to all the keys
    """
    similarity_vector = np.dot(keys, _id)
    highest_similarity = max(similarity_vector)
    best_key_idx = np.where( similarity_vector == highest_similarity)
    best_key = keys[best_key_idx]
    return best_key



