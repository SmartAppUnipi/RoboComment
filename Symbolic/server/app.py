import flask
from json_validator import Validator
import json
import requests
from time import sleep
from flask import render_template,jsonify
from server.map2d import *


app = flask.Flask(__name__)
debug_map = None
_WIDTH = 1200
_HEIGHT = 752

"""-------------AGGIUNTI ENDPOINT PER COMUNICARE CON LA PARTE CLIENT DELLA MAPPA----------"""
@app.route("/debug")
def init_map():
    return render_template('page_map.html')


@app.route("/debug/positions")
def _get_positions():
    global debug_map
    if debug_map is None:
        debug_map = Map2d(_WIDTH,_HEIGHT,build_fake_map(_WIDTH,_HEIGHT))
    return debug_map._get_map_json()

"-------------------------------------------------------------"

@app.route("/")
def welcome():
   return "Symbolic Level"

@app.route("/pos")
def pos():
    return jsonify({'x':100,'y':200})

@app.route('/positions', methods=['POST'])
def new_positions(second):

    data = flask.request.form

    print("##############")
    print(data)
    print("##############")

    if Validator.validate_positions(data):
        print("Data is correctly formatted")
    else: 
        print("data is incorrect:")
        print(data)
        print("########################")
    
    # validate input json and execute business logic code
    with open('../tests/dummy.json', 'r') as f: 
        dummy = json.load(f) 

    cg_url = cg_host + ":" + str(cg_port) + "/api/action"
    print(cg_url)
    print(dummy[2])
    requests.post(cg_url, json=dummy[2])

    return "ciao"


if __name__ == '__main__':
    with open('config.json', 'r') as f: 
        config = json.load(f) 
        symbolic_port = config['symbolic-port']
        cg_host = config["comment-generation-host"] 
        cg_port = config["comment-generation-port"]

    #app.run(debug=True)
    app.run(host='0.0.0.0', port=symbolic_port, debug=True)
    #app.run(debug=True) #CON L'IP 0.0.0.0 non mi faceva visualizzare la pagina web (probabilmente x firewall)
