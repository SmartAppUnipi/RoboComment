import flask
from json_validator import Validator

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
    app.run(port=3000, debug=True)

