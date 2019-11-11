import flask
from json_validator import Validator
import json
import requests

app = flask.Flask(__name__)

@app.route("/")
def welcome():
    return "Symbolic Level"

@app.route('/positions/<int:second>', methods=['POST'])
def new_positions(second):

    data = flask.request.form

    print("##############")
    print(data)
    print("##############")

    #Validator.validate_positions(data)
    
    # validate input json and execute business logic code
    with open('../tests/dummy.json', 'r') as f: 
        dummy = json.load(f) 

    cg_url = cg_host + ":" + str(cg_port) + "/api/action"
    print(cg_url)
    print(dummy[2])
    requests.post(cg_url, json=dummy[2])

    return "ciao"


if __name__ == '__main__':
    with open('config.json', 'r') as f: 
        config = json.load(f) 
        symbolic_port = config['symbolic-port']
        cg_host = config["comment-generation-host"] 
        cg_port = config["comment-generation-port"]

    app.run(host='0.0.0.0', port=symbolic_port, debug=True)

