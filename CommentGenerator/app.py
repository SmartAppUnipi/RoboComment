from flask import Flask, request
import json
import requests
import sys
from src.Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
from threading import Thread

app = Flask(__name__)

AUDIO_IP = "x.x.x.x"
AUDIO_PORT = "3003"
KB_IP = "x.x.x.x"
KB_PORT = "3004"

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
            response = requests.post(url="http://" + AUDIO_IP + ":" + AUDIO_PORT + "/", json=output, headers=headers)
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

    knowledge_base = KnowledgeBase(url=KB_IP + ":" + KB_PORT)
    commentator = Commentator(knowledge_base)

if __name__ == '__main__':
    try:
        with open("services.json",'r') as servicesfile:
            services = json.load(servicesfile)

            AUDIO_IP = services['audio.output']['host']
            AUDIO_PORT = str(services['audio.output']['port'])
            KB_IP = services['knowledgebase']['host']
            KB_PORT = str(services['knowledgebase']['port'])
    
    except FileNotFoundError:
        print("No services.json file provided")
    
    
    # try:
    #     AUDIO_IP = sys.argv[1]
    #     KB_URL = sys.argv[2]
    # except IndexError:
    #     print("USAGE: python3.6 app.py [AUDIO IP] [KB IP]")
    #     exit(-1)
    
    app.run(host='0.0.0.0', port=3002)
