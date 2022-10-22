import numpy as np
import json


class Message:
        
    def __init__(self, message:str, chunk_size:int):

        self.chunk_size = chunk_size
        self.message = message # Client's message
        self.message_vector = transform_message(message) # Transformed message into bipolar vector
        self.chunks = divide_to_chunks(
            vector= self.message_vector,
            chunk_size= self.chunk_size
            )
        
    # Encryp chunk data by incorporating client ID: *Data = (Data * Id ) + Id
    def encrypt(self, _id: np.array) -> list:
        encrypted_chunks =  [ (np.multiply(chunk, _id) + _id) for chunk in self.chunks] # Perform encryption on each chunk
        return encrypted_chunks # Return the encrypted chunks in a list

    def decrypt(self, ):
        pass
            

# Divide original message into smaller chunks
def divide_to_chunks(vector: np.array, chunk_size:int):
    length = len(vector) # Get vector size
    chunks = [vector[x: x+ chunk_size] for x in range(0, length, chunk_size)] # Divide vector into chunks
    last_chunk = list(chunks[-1]) # Size of the last chunk is usually same as other chunks, or smaller
    size = len(last_chunk) # Get size of last chunk
    n_to_fill = chunk_size - size # Get of required number bits to fill the rest
    if n_to_fill: # Handle the last chunk if incomplete
        new_chunk = last_chunk + [-1 for i in range(n_to_fill)] # Fill the last with -1
        chunks[-1] = np.array(new_chunk) # Update last element of chunk list with the new completed size chunk
    return chunks # Return chunk


# Transform a String message into a numpy array binary vector
def transform_message(msg:str) -> np.array:
    binary_vector = []
    for charac in msg: # For each character in string message e.g = "Hello"
        charac_ascii = ord(charac) # Get ASCI value of the string    First charac=H => charac_ascii = 72
        charac_binary = ''.join(format(charac_ascii, 'b')) # Transform 72 to "1001000"
        binary_vector.extend([int(bit) for bit in list(charac_binary)]) # Split "1001000" to zeros and ones, and append it to binary vector 
    bipolar_vector = np.array([ val if val == 1 else -1 for val in binary_vector]) # Transform into bipoler values
    return bipolar_vector

# Encode numpy values to JSON
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)