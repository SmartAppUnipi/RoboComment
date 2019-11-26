from flask import Flask, request
import json
import requests
import sys
from src.Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
from threading import Thread

app = Flask(__name__)

AUDIO_IP = "x.x.x.x"
KB_URL = "x.x.x.x:xxxx"
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
            response = requests.post(url="http://" + AUDIO_IP + ":3003/", json=output, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Audio unreachable at " + AUDIO_IP)
        
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
    # call our main

    output = commentator.run(input)
    
    print(output['comment'])
    # post to the audio group
    forward_to_audio(output)
    
    return "OK"


@app.before_first_request
def init():
    ''' this function will be called at the application startup to initialize our module '''
    global knowledge_base
    global commentator

    knowledge_base = KnowledgeBase(url=KB_URL)
    commentator = Commentator(knowledge_base)

if __name__ == '__main__':
    try:
        AUDIO_IP = sys.argv[1]
        KB_URL = sys.argv[2]
    except IndexError:
        print("USAGE: python3.6 app.py [AUDIO IP] [KB IP]")
        exit(-1)
    
    app.run(host='0.0.0.0', port=3002)
