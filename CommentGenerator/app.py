from flask import Flask, request
import json
import requests
import sys
from src.Commentator import Commentator

app = Flask(__name__)

AUDIO_IP = ""
commentator = None

@app.route('/api', methods=['GET'])
def api():
    return "Hi! the server is alive!"


@app.route('/api/action', methods=['POST'])
def action():
    input = json.loads(request.data)
    print(input)
    # call our main
    
    output = commentator.run(input)
    # post to the audio group
    response = requests.post(url="http://" + AUDIO_IP + ":3003/", data=json.dumps(output))
    return "OK"


# Simulazione Gruppo Audio
@app.route('/test/audio', methods=['POST'])
def test():
    action_json = json.loads(request.data)
    print(action_json)
    return "OK"


if __name__ == '__main__':
    AUDIO_IP = sys.argv[1]
    commentator = Commentator('assets/config_test.json', 'assets/templates.json')
    app.run(host='0.0.0.0', port=3002)
