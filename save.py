# Autosave microservice

import time
import zmq
import json

context = zmq.Context()             # Sets up the environment so that we are able to begin
socket = context.socket(zmq.REP)    # Reply socket type
socket.bind("tcp://*:5556")         # Set to listen on port 5556


def save_game_data(slot, data):
    """
    Saves game state
    """
    with open(f'save_slot_{slot}.json', "w") as file:
        json.dump(data["data"], file, indent=4)

    return True

def load_game_data(slot):
    """
    Sends back load data
    """
    with open(f'save_slot_{slot}.json', "r") as file:
        load_data = json.load(file)
    return load_data


while True:
    data = socket.recv_json()  # Where the message will be held
    response = None

    if data:
        if data['request'] == 'save':
            print('Save request received')
            response = save_game_data(data['slot'], data)
            socket.send_string(str(response))
            print('Save successful')

        if data['request'] == 'load':
            print('Load request received')
            response = load_game_data(data['slot'])
            socket.send_json(response)
            print('Data successful sent')

        time.sleep(2)
