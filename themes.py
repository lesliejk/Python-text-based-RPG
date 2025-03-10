
import time
import zmq
import base64

context = zmq.Context()             # Sets up the environment so that we are able to begin
socket = context.socket(zmq.REP)    # Reply socket type
socket.bind("tcp://*:5557")         # Set to listen on port 5557


def retrieve_sound(theme):
    """
    Retrieves image and returns as byte string
    """
    sound = open('themes/' + theme + '.mp3', 'rb').read()
    byte_sounds = base64.b64encode(sound)
    return byte_sounds


while True:
    data = socket.recv_json()  # Where the message will be held
    response = None

    if data:
        print('Request received')
        response = retrieve_sound(data['theme'])
        socket.send(response)
        print('Sound file delivered')

        time.sleep(1)