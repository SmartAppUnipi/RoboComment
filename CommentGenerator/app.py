from flask import Flask, request
import json
import requests
import sys
from src.CommentatorPool import CommentatorPool
from utils.KnowledgeBase import KnowledgeBase
from threading import Thread
import logging

app = Flask(__name__)

AUDIO_URL = "http://audio.url:3003/"
KB_URL = "http://kb.url:3004/"
commentator_pool = None

@app.route('/api', methods=['GET'])
def api():
    ''' this interface can be used to check if the server is up and running '''
    return "Hi! the server is alive!"


def send_to_audio(output):
    ''' this function will send our output to the audio'''
    print("OUTPUT:: " + output['comment'])
    logging.info(output)
    headers = {'Content-type': 'application/json'}
    try:
        response = requests.post(url=AUDIO_URL, json=output, headers=headers)
    except requests.exceptions.ConnectionError:
        print("Audio unreachable at " + AUDIO_URL)

@app.route('/api/action', methods=['POST'])
def action():
    ''' 
        it gets a json from the symbolic group, and forwards it to the right commentator
    '''
    global commentator_pool

    input = json.loads(request.data)
    print("INPUT:: " + json.dumps(input))
    logging.info(input)

    commentator_pool.push_symbolic_event_to_match(42,input) #TODO fix this 42, it should be get from the json

    return "OK"

@app.route('/api/session/start/<int:matchid>/<int:userid>', methods=['POST'])
def session_start(matchid,userid):
    ''' this method will be called by the audio each time a new user watches a match'''
    global commentator_pool
    
    commentator_pool.start_session(matchid,userid)
    return "OK"

@app.route('/api/session/end/<int:matchid>/<int:userid>', methods=['POST'])
def session_end(matchid,userid):
    ''' this method will be called by the audio each time a user ends the video streaming'''
    global commentator_pool

    commentator_pool.end_session(matchid,userid)
    return "OK"


@app.before_first_request
def init():
    ''' this function will be called at the application startup to initialize our module '''
    global commentator_pool

    logging.basicConfig(filename='CommentGenerator/commentgenerator.log',level=logging.INFO) # filemode='w'

    commentator_pool = CommentatorPool(KB_URL,send_to_audio)

if __name__ == '__main__':
    try:
        with open("routes.json",'r') as servicesfile:
            services = json.load(servicesfile)
            AUDIO_URL = services['fabula']
            KB_URL = services['qi']
    
    except FileNotFoundError:
        print("No routes.json file provided")
    
    app.run(host='0.0.0.0', port=3002)
