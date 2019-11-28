from flask import Flask, request
import json
import requests
import sys
from src.Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
from threading import Thread
import logging

app = Flask(__name__)

AUDIO_URL = "http://audio.url:3003/"
KB_URL = "http://kb.url:3004/"
commentator = None
knowledge_base = None

@app.route('/api', methods=['GET'])
def api():
    ''' this interface can be used to check if the server is up and running '''
    return "Hi! the server is alive!"


def forward_to_audio(output):
    ''' this function will send our output to the audio in an async waiy, in order to responde immediatly to the symbolic level'''
    def async_request():
        headers = {'Content-type': 'application/json'}
        try:
            response = requests.post(url=AUDIO_URL, json=output, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Audio unreachable at " + AUDIO_URL)
        
    t = Thread(target=async_request)
    t.start()


@app.route('/api/action', methods=['POST'])
def action():
    ''' 
        it gets a json from the symbolic group, calls our internal modules to produce a comment and
        sends it to the audio group
    '''
    global commentator
    input = json.loads(request.data)
    print(input)
    logging.info(input)
    # call our main

    output = commentator.run(input)
    
    print(output['comment'])
    logging.info(output)
    # post to the audio group
    forward_to_audio(output)
    
    return "OK"


@app.before_first_request
def init():
    ''' this function will be called at the application startup to initialize our module '''
    global knowledge_base
    global commentator

    logging.basicConfig(filename='CommentGenerator/commentgenerator.log',level=logging.INFO) # filemode='w'
     
    knowledge_base = KnowledgeBase(url=KB_URL)
    commentator = Commentator(knowledge_base)

if __name__ == '__main__':
    try:
        with open("routes.json",'r') as servicesfile:
            services = json.load(servicesfile)
            AUDIO_URL = services['fabula']
            KB_URL = services['qi']
    
    except FileNotFoundError:
        print("No routes.json file provided")
    
    app.run(host='0.0.0.0', port=3002)
