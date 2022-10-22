import numpy as np



def maximum_similarity(chunk:np.array, keys: np.array):
    similarity_vector = np.dot(keys, chunk) # Compute similarity vector by using DOT product
    max_sim = max(similarity_vector) # Get the highest similarity value
    max_sim_idx = np.where(similarity_vector == max_sim)
    max_sim_entry = max_sim_idx[0][0] + 1
    max_sim_key = keys[max_sim_idx][0] # Key with highest similarity value
    return max_sim, max_sim_key, max_sim_entry


def match_id_to_key(_id:np.array, keys: np.array):
    """
    This function computes the DOT product of the received ID to all the keys
    """
    similarity_vector = np.dot(keys, _id)
    highest_similarity = max(similarity_vector)
    best_key_idx = np.where( similarity_vector == highest_similarity)
    best_key = keys[best_key_idx]
    return best_key




