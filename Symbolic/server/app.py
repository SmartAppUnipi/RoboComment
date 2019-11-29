import flask
from json_validator import Validator
import json
import requests

app = flask.Flask(__name__)

@app.route("/")
def welcome():
    return "Symbolic Level"

@app.route('/positions', methods=['POST'])
def new_positions():

    data = flask.request.form

    print("##############")
    print(data)
    print("##############")

    if Validator.validate_positions(data):
        print("Data is correctly formatted")
    else: 
        print("data is incorrect:")
        print(data)
        print("########################")
    
    # validate input json and execute business logic code

    print("sending to ", cg_url)
    print(dummy[2])
    requests.post(cg_url, json=dummy[2])

    return ""


if __name__ == '__main__':
    with open('../../routes.json', 'r') as f: 
        config = json.load(f) 
        symbolic_port = 3001
        cg_url = config['tale']

    with open('../tests/dummy.json', 'r') as f: 
        dummy = json.load(f) 

    app.run(host='0.0.0.0', port=symbolic_port, debug=True)

