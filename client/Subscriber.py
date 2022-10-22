import sys
import json
import requests
import numpy as np
import random

from flask import Flask, request, Response, render_template
from Message import Message, NpEncoder
from Vector import Vector

CHUNK_SIZE = 1001

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8080



def main(argv): # Takes as arguments the publisher network information from terminal e.g python Publisher.py 127.0.0.1:5000

    client_args = argv[0].split(":") # ["127.0.0.1", "5000"]
    CLIENT_ADDRESS = client_args[0] # Address
    CLIENT_PORT = int(client_args[1]) # Port number
    _id = Vector(np.array([ random.randint(0, 1) for i in range(CHUNK_SIZE)])) # Generate vector ID
    print(f"My SUBSCRIBER ID in ASCII format is: {_id.to_ascii()}") 

    app = Flask(__name__) # Flask app


    # Render home page of publisher
    @app.route('/')
    def index():
        return render_template("subscriber.html", data="", _id=_id.to_ascii())


    # Subscribe to client's data to the server
    @app.route('/subscribe', methods=['GET'])
    def subscribe():
        #requested_id = request.form.get("requested_id") # Get user input from GUI
        requested_id = "109_106_83_75_33_61_83_98_29_78_54_50_45_8_54_22_8_4_102_90_64_60_22_103_58_80_85_125_15_103_25_35_122_117_99_21_104_37_116_67_6_66_48_33_123_39_0_15_45_72_2_104_56_114_81_54_49_25_123_95_28_108_55_93_126_54_21_82_8_74_26_20_43_78_25_27_70_86_6_39_104_15_25_57_99_106_71_108_100_12_62_73_40_56_70_114_116_99_66_67_43_66_81_36_18_110_99_80_127_27_91_82_96_16_45_72_5_8_39_94_84_111_17_81_37_111_113_101_32_78_118_1_18_60_54_77_43_42_16_96_50_78_18"
        url = f"http://{SERVER_ADDRESS}:{SERVER_PORT}/getData?id={requested_id}" # Define the server's URL + endpoint
        
        if requested_id:
            print(requested_id)

        return render_template("subscriber.html")
        
        """
        if message: # Check if message is empty
            msg = Message(message = message , chunk_size = CHUNK_SIZE) # Instanciate the Message class
            encrypted_chunks = msg.encrypt(_id = _id.to_bipolar()) # Encrypt the message by embedding the ID

            for chunk in encrypted_chunks: # encrypted_chunks is a list of all encrypted chunks 
                response = requests.post(url, json = json.dumps(chunk, cls=NpEncoder)) # Post each chunk
                print(response.text) # Server replies back "Chunk received!"

            return render_template("publisher.html", data="Successful publish of message.", _id=_id.to_ascii())

        else:
            return render_template("publisher.html", data="Write a message to send!", _id=_id.to_ascii())
        """





    app.run(debug=True, host=CLIENT_ADDRESS, port=CLIENT_PORT)

if __name__ == "__main__":
    main(sys.argv[1:])


