import flask
from server.json_validator import Validator
import json
import requests

app = flask.Flask(__name__)

@app.route("/")
def welcome():
    return "Symbolic Level"

@app.route('/positions/<int:second>', methods=['POST'])
def new_positions():
    data = flask.request.form
    Validator.validate_positions(data)
    print(data)
    # validate input json and execute business logic code
    with open('tests/dummy.json', 'r') as f: 
        dummy = json.load(f) 
    cg_url = cg_url + ":" + str(cg_port) + "/api/action"
    print(cg_url)
    requests.post(cg_url, json=dummy[2])


if __name__ == '__main__':
    with open('server/config.json', 'r') as f: 
        config = json.load(f) 
        symbolic_port = config['symbolic-port']
        cg_host = config["comment-generation-host"] 
        cg_port = config["comment-generation-port"]

    app.run(host='0.0.0.0', port=symbolic_port, debug=True)

