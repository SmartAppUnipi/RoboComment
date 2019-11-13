from flask import Flask, request
import json
import requests
import sys
from CommentGenerator.src.Commentator import Commentator

app = Flask(__name__)

AUDIO_IP = "x.x.x.x"
commentator = None


@app.route('/api', methods=['GET'])
def api():
    ''' this interface can be used to check if the server is up and running '''
    return "Hi! the server is alive!"


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

    # post to the audio group
    headers = {'Content-type': 'application/json'}
    try:
        response = requests.post(url="http://" + AUDIO_IP + ":3003/", json=output, headers=headers)
    except requests.exceptions.ConnectionError:
        print("Audio unreachable at " + AUDIO_IP)

    return "OK"


# Simulazione Gruppo Audio
@app.route('/test/audio', methods=['POST'])
def test():
    ''' just to simulate the audio interface, this function must disappear in a production env'''
    action_json = json.loads(request.data)
    print(action_json)
    return "OK"


@app.before_first_request
def init():
    ''' this function will be called at the application startup to initialize our module '''
    global commentator
    commentator = Commentator()


if __name__ == '__main__':
    try:
        AUDIO_IP = sys.argv[1]
    except IndexError:
        print("USAGE: python3.6 app.py [AUDIO IP]")
        exit(-1)

    commentator = Commentator()
    app.run(host='0.0.0.0', port=3002)
