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

#DIMENSIONI IN METRI DEL CAMPO... FARLI PASSARE DA QUALCUNO...
_WIDTH = 105
_HEIGHT = 68
map = Map2d(_WIDTH, _HEIGHT, [], socketio)


_DEBUG = False

debug_map = None
_N_ITERS_TEST = 0

pp = pprint.PrettyPrinter(indent=4)

"""-------------AGGIUNTI ENDPOINT PER COMUNICARE CON LA PARTE CLIENT DELLA MAPPA----------"""
#Avvia la simulazione della mappa (atteso input dopo che arriva il json da video processing)
@app.route("/debug")
def init_map():
    global _DEBUG
    _DEBUG = False
    return render_template('page_map.html')

#Endpoint usato SOLO per testare la mappa
@app.route("/debug/test/<int:n>")
def test_map(n):
    global socketio
    global _DEBUG
    global _N_ITERS_TEST

    _DEBUG = True
    _N_ITERS_TEST = n
    socketio.on_event('notify',handle)
    return render_template('page_map.html')

"""---------------------FUNZIONI USATE X DEBUG DELLA MAPPA--------------"""

def update_periodic(socketio):
    global debug_map
    global _DEBUG
    global _WIDTH
    global _HEIGHT
    global _N_ITERS_TEST

    dummy_new = copy.deepcopy(dummy[0])
    debug_map = Map2d(_WIDTH,_HEIGHT,dummy_new,socketio,_DEBUG)
    debug_map._send_init_position()
    for i in range(_N_ITERS_TEST):
        sleep(1)
        for j in range(random.randint(1,22)):
            dummy_new = move_player(dummy_new,random.randint(1,11),random.randint(0,1),random.uniform(-5,5),random.uniform(-5,5))
        dummy_new = move_ball(dummy_new,random.uniform(-5,5),random.uniform(-5,5))

        for j in range(random.randint(1,5)):
            dummy_new = modify_id_confidence(dummy_new,random.randint(1,11),random.randint(0,1),random.uniform(0,1))
            dummy_new = modify_team_confidence(dummy_new,random.randint(1,11),random.randint(0,1),random.uniform(0,1))
        
        dummy_new = move_player(dummy_new,4,-1,random.uniform(-10,10),random.uniform(-10,10))
        
        debug_map._update_position(dummy_new)
   

def handle(message):
    global _DEBUG
    if _DEBUG:
        x = threading.Thread(target=update_periodic,args=(socketio,))
        x.start()
    
"---------------------------------------------------------------------------------"


"-------------------------------------------------------------"

@app.route("/")
def welcome():
   return "Symbolic Level"

@app.route("/pos")
def pos():
    return jsonify({'x':100,'y':200})

@app.route('/positions', methods=['POST'])
def new_positions(second):
    global model

    data = flask.request.form

    print("Received data from video processing")

    if Validator.validate_positions(data):
        print("Data is correctly formatted")
    else: 
        print("data is incorrect")

    model.new_positions(data)

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