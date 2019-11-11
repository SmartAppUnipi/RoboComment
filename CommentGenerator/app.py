from flask import Flask, request
import json
import requests
from Commentator import Commentator

app = Flask(__name__)

AUDIO_URL = "http://127.0.0.1:5555/api/test"


@app.route('/api', methods=['GET'])
def api():
    return "Hi! the server is alive!"


@app.route('/api/action', methods=['POST'])
def action():
    input = json.loads(request.data)
    print(input)
    # call our main
    commentator = Commentator('assets/config_test.json', 'assets/templates.json')
    output = commentator.run(input)
    # post to the audio group
    response = requests.post(url=AUDIO_URL, data=json.dumps(output))
    return "OK"


# Simulazione Gruppo Audio
@app.route('/api/test', methods=['POST'])
def test():
    action_json = json.loads(request.data)
    print(action_json)
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
