from flask import Flask, request
import json
import requests
import sys
from src.Commentator import Commentator

app = Flask(__name__)

AUDIO_IP = "x.x.x.x"
commentator = None

@app.route('/api', methods=['GET'])
def api():
    return "Hi! the server is alive!"


@app.route('/api/action', methods=['POST'])
def action():
    global commentator
    input = json.loads(request.data)
    print(input)
    # call our main
    
    output = commentator.run(input)
    # post to the audio group
    try:
        requests.post(url="http://" + AUDIO_IP + ":3003/", data=json.dumps(output))
    except requests.exceptions.ConnectionError:
        print("audio unreachable at " + AUDIO_IP )

    return "OK"


# Simulazione Gruppo Audio
@app.route('/test/audio', methods=['POST'])
def test():
    action_json = json.loads(request.data)
    print(action_json)
    return "OK"


@app.before_first_request
def init():
    global commentator
    commentator = Commentator()

if __name__ == '__main__':
    try:
        AUDIO_IP = sys.argv[1]
        app.run(host='0.0.0.0', port=3002)
    except IndexError:
        print("ERROR: insert ip as parameter")
