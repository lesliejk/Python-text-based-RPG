# Image microservice

import time
import zmq
import base64

context = zmq.Context()             # Sets up the environment so that we are able to begin
socket = context.socket(zmq.REP)    # Reply socket type
socket.bind("tcp://*:5555")         # Set to listen on port 5555


def retrieve_image(type, name):
    """
    Retrieves image and returns as byte string
    """
    image = open('images/' + type + '/' + name.lower().strip() + '.jpg', 'rb').read()
    byte_image = base64.b64encode(image)
    return byte_image


while True:
    data = socket.recv_json()  # Where the message will be held
    response = None

    if data:
        print('Request received')
        response = retrieve_image(data['type'], data['name'])
        socket.send(response)
        print('Image delivered')

        time.sleep(1)
