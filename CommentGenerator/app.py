from flask import Flask, request
import json
import requests
app = Flask(__name__)

AUDIO_URL  = "http://0.0.0.0:5555/test"

@app.route('/api', methods=['GET'])
def api():
    return "Hi! the server is alive!" 


@app.route('/api/action',methods=['POST'])
def action():

    action_json = json.loads(request.data)
    print(action_json)
    
    # call our main
        
    # post to the audio group
    response = requests.post(url=AUDIO_URL, data=json.dumps(action_json))
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555)