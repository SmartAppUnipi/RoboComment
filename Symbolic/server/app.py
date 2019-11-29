import flask
from json_validator import Validator
import json
import requests
from time import sleep, time
from flask import render_template, jsonify, request
from map2d import *
from flask_socketio import SocketIO, emit
import pprint
import threading
import os
import random
from dummy_map import *
import copy
from sched import scheduler
from game_model.game_model import GameModel, U
import game_model.interpreter.set_rule_matcher


app = flask.Flask(__name__)
socketio = SocketIO(app)

# DIMENSIONI IN METRI DEL CAMPO...
_WIDTH = 105
_HEIGHT = 68

map = Map2d(_WIDTH, _HEIGHT, socketio)
pp = pprint.PrettyPrinter(indent=4)


# Avvia la simulazione della mappa (atteso input dopo che arriva il json da video processing)
@app.route("/debug", methods=['GET'])
def init_map():
    if request.method == 'GET':
        return render_template('page_map.html')


@app.route("/stacks", methods=['POST', 'GET'])
def stacks():
    env = GameModel.get_env()
    if request.method == 'GET':
        return render_template('stacks.html', data=env['stacks'])
    elif request.method == 'POST':
        return 200


@app.route("/")
def welcome():
    return "Symbolic Level"


@app.route('/positions', methods=['POST'])
def new_positions():
    global map

    data = flask.request.json

    print("Received data from video processing")
    if Validator.validate_positions(data):
        print("Data is correctly formatted")
    else:
        print("data is incorrect")

    # Metto in map le nuove posizioni
    map._update_position(data)
    U.new_positions(data)


    with open('positions.out', 'a+') as dump_file:
        string = json.dumps(data, separators=(',', ':'))
        dump_file.write(string+"\n")
    return ""


if __name__ == '__main__':
    if os.path.exists("positions.out"):
        os.remove("positions.out")

    print("app is running, open localhost:3001/debug to display the map")
    socketio.run(app, host='0.0.0.0',
                 use_reloader=False, port=3001)
