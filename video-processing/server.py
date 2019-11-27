import os
import json
import re
from flask import Flask
from flask_cors import CORS
import requests


class RoutesParser:
    def __init__(self, path=None):
        if path is None:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../routes.json")
        self.routes = json.load(open(path))

    def post(self, name, data):
        r = requests.post(url=self.routes[name], data=data)
        return r.status_code

    def __getitem__(self, name):
        m = re.match(r"(https?:\/\/)(.*):(\d*)(\/?.*)", self.routes[name])
        host = m.group(2)
        port = int(m.group(3))
        path = m.group(4)
        return host, port, path


app = Flask(__name__)
CORS(app)

routes = RoutesParser()
_, port, path = routes["video"]
sym_host, sym_port, sym_path = routes["scene"]

print(f"Running on port {port} at {path}(POST)")


@app.route(path, methods=["POST"])
def post_video():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mocks/dummy.json"), "r") as f:
        data = json.load(f)

    for x in data:
        code = routes.post("scene", x)
        print(f"Symbolic response code {code}")

    return "ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
