import numpy as np
import random




def dot_product(x, y):
    """
    A = np.array([[1,-1, 1, -1],[1, -1, 1, 1], [-1, 1, -1, 1]]) 
    b = np.array([1, -1, -1, 1]) 
    result = A*b = array([0, 2, 0])
    """
    return np.dot(x, y)

    
def transform_message(msg:str) -> np.array:
    """
    
    """
    binary_msg = msg_to_binary(msg)
    bipolar_msg = binary_to_bipolar(binary_msg)
    return bipolar_msg


def msg_to_binary(msg:str) -> np.array :
    """
    Transform a String message into a numpy array binary vector
        For each character in string message e.g = "Hello"
        Get ASCI value of the string    First charac=H => charac_ascii = 72
        We transform 72 to "1001000"
        We split "1001000" to zeros and ones, and append it to binary vector        
    """
    binary_vector = []
    for charac in msg: 
        charac_ascii = ord(charac) 
        charac_binary = ''.join(format(charac_ascii, 'b')) 
        binary_vector.extend([int(bit) for bit in list(charac_binary)]) 
    return np.array(binary_vector)

def binary_to_string(binary_vector:list):
    binary_string = ''.join([str(val) for val in binary_vector])
    return binary_string


def binary_to_ascii(binary_vector:list):
    """
    Transform binary vector e.g [1, 1, 0, 1] to integer value 
    """
    binary_string = ''.join([str(val) for val in binary_vector])
    return int(binary_string, 2)

def ascii_to_binary(ascii_val:int):
    """
    Transform ascii_value e.g 130 to binary 
    """
    binary_string = ''.join([str(val) for val in binary_vector])
    return int(binary_string, 2)

def binary_to_bipolar(binary_vector:np.array) -> np.array:
    """
    Transform a binary vector into a bipolar vector
    Replace every 0 value by -1
    """
    return np.array([ val if val == 1 else -1 for val in binary_vector])

def bipolar_to_binary(bipolar_vector:np.array) -> np.array:
    """
    Transform a binary vector into a bipolar vector
    Replace every 0 value by -1
    """
    return np.array([ val if val == 1 else 0 for val in binary_vector])

def divide_to_chunks(vector: np.array, chunk_size:int):
    """
    When dividing data into chunks, the size of the last vector is usually same as other chunks, or smaller
    We handle the last chunk if incomplete, by appending -1 values to the rest of the vector 
    """
    length = len(vector)
    chunks = [vector[x: x+ chunk_size] for x in range(0, length, chunk_size)]
    last_chunk = list(chunks[-1])
    size = len(last_chunk)
    n_to_fill = chunk_size - size
    if n_to_fill:
        new_chunk = last_chunk + [-1 for i in range(n_to_fill)]
        chunks[-1] = np.array(new_chunk)
    return chunks


def generate_id(dimension:int):
    binary_id = np.array([ random.randint(0, 1) for i in range(dimension)])
    divided_id = [binary_id[x: x+ 7] for x in range(0, dimension, 7)]
    _id_ascii = [ binary_to_ascii(vector_7bits) for vector_7bits in divided_id]
    _id = binary_to_bipolar(binary_id)
    return _id, _id_ascii




