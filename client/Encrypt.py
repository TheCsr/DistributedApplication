import numpy as np
import json
from helper import transform_message, divide_to_chunks


class EncryptMessage:
    
    
    def __init__(self, message:str, chunk_size:int):
        """
        This data class structure 

        """
        self.chunk_size = chunk_size
        self.message = message # Client's message
        self.message_vector = transform_message(message) # Transformed message into bipolar vector
        self.length = len(self.message_vector) # Length of the WHOLE message vector
        self.chunks = divide_to_chunks(
            vector= self.message_vector,
            chunk_size= self.chunk_size
            )
        

    
    def encrypt(self, _id: np.array) -> list:
        """
        This method takes as input the client's Id
        Return the encrypted message which is *Data = (Data * Id ) + Id
        Bipolar data is used 
        """
        self.encrypted_chunks = [ (np.multiply(chunk, _id) + _id) for chunk in self.chunks]            
            


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)