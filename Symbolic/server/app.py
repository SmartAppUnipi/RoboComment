import flask
from server.json_validator import Validator
import json

app = flask.Flask(__name__)

@app.route("/")
def welcome():
    return "Symbolic Level"

@app.route('/positions/<int:second>', methods=['POST'])
def new_positions():
    data = flask.request.form
    Validator.validate_positions(data)
    players = data['players']
    ball = data['ball']
    referee = data['referee']
    # validate input json and execute business logic code

if __name__ == '__main__':
    with open('server/config.json', 'r') as f: 
        config = json.load(f) 
        print(config['port'])
    app.run(host='0.0.0.0', port=config['port'], debug=True)

