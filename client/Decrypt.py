import numpy as np
import json


class DecryptMessage:

    def __init__(self, encrypted_chunks: np.array, chunk_size:int):
        self.encrypted_chunks = encrypted_chunks
        self.chunk_size = chunk_size
        
    def decrypt(self, _id:np.array):
        padding_size = self.chunk_size % 7
        data_size = self.chunk_size - padding_size

        binary_data = []
        for chunk in self.encrypted_chunks:

            decrypted_chunk = decrypt(chunk, _id ) # Decrypt data
            decrypted_chunk = bipolar_to_binary(decrypted_chunk)    
            decrypted_chunk = binary_to_string(decrypted_chunk)
            
            last_charac = decrypted_chunk[-1]
            if last_charac == "0":
                n_zeros = 0
                for charac in reversed(decrypted_chunk):
                    if charac == "0":
                        n_zeros+=1
                    if charac == "1":
                        break
                decrypted_chunk = decrypted_chunk[:(data_size-n_zeros)]
                binary_data.append(decrypted_chunk)        
            else:
                decrypted_chunk = decrypted_chunk[:data_size]
                binary_data.append(decrypted_chunk)

        binary_string = "".join(binary_data)
        decrypted_messages = to_ascii(binary_string, len(binary_string))
        return decrypted_messages


def decrypt(chunk: np.array, _id:np.array):
    decrypted = (chunk - _id) / _id
    decrypted = np.array([int(val) for val in decrypted])
    return decrypted

def bipolar_to_binary(bipolar_vector:np.array) -> np.array:
    """
    Transform a binary vector into a bipolar vector
    Replace every 0 value by -1
    """
    return np.array([ val if val == 1 else 0 for val in bipolar_vector])

def binary_to_string(binary_vector: np.array):
    return ''.join([str(x) for x in binary_vector])

def to_ascii(str_message:str, chunk_size:int):
    characters = [chr(int(str_message[i:i+7], 2)) for i in range(0, chunk_size, 7)]    
    return "".join(characters)


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