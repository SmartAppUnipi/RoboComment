import flask
from json_validator import Validator
import json
import requests
from time import sleep, time
from flask import render_template,jsonify
from map2d import *
from flask_socketio import SocketIO,emit
import pprint
import threading
import random
from dummy_map import *
import copy
from sched import scheduler
from game_model.game_model import GameModel


app = flask.Flask(__name__)
socketio = SocketIO(app)

model = None

#DIMENSIONI IN METRI DEL CAMPO...
_WIDTH = 105
_HEIGHT = 68

map = Map2d(_WIDTH, _HEIGHT,socketio)
pp = pprint.PrettyPrinter(indent=4)


#Avvia la simulazione della mappa (atteso input dopo che arriva il json da video processing)
@app.route("/debug")
def init_map():
    return render_template('page_map.html')

@app.route("/")
def welcome():
   return "Symbolic Level"

@app.route('/positions', methods=['POST'])
def new_positions():
    global model
    global map

    data = flask.request.json 

    print("Received data from video processing")
    if Validator.validate_positions(data):
        print("Data is correctly formatted")
    else: 
        print("data is incorrect")

    #Metto in map le nuove posizioni
    map._update_position(data)
    model.new_positions(data)

    with open('positions.out', 'a+') as dump_file:
        string = json.dumps(data, separators=(',',':'))
        dump_file.write(data)
    return ""

def main():
    global model
    with open('../../routes.json', 'r') as f: 
        config = json.load(f) 
        symbolic_port = 3001
        cg_url = config['tale']

    model = GameModel(cg_url)

    print("app is running, open localhost:3001/debug to display the map")
    socketio.run(app, host='0.0.0.0', use_reloader=False, port=symbolic_port)

if __name__ == '__main__':
    main()