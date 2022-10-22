import numpy as np

class Vector:

    def __init__(self, binary_vector:np.array):
        self.binary_vector =  binary_vector      
        
    def to_string(self) -> np.array:
        return ''.join([str(val) for val in self.binary_vector])


    def to_bipolar(self) -> np.array:
        """
        Transform a binary vector into a bipolar vector
        Replace every 0 value by -1
        """
        return np.array([ val if val == 1 else -1 for val in self.binary_vector])
    
    def to_ascii(self) -> list:
        dimension = len(self.binary_vector)
        divided_id = [self.binary_vector[x: x+ 7] for x in range(0, dimension, 7)]
        ascii_values = [ int(''.join([str(val) for val in vector_7bits]), 2)  for vector_7bits in divided_id]
        return "_".join([ str(_) for _ in ascii_values])


