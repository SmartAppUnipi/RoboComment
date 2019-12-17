import json
import os
import re

import requests

class RoutesParser:
    def __init__(self, path=None):
        if path is None:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../routes.json")
            path = os.path.abspath(path)
        self.routes = json.load(open(path))

    def post(self, name, data):
        r = requests.post(url=self.routes[name], json=data)
        return r.status_code


    def query_kb(self, name, service, id_):
        url = self.routes[name] + service + "/" + str(id_)
        r = requests.get(url)
        return r.json()


    def __getitem__(self, name):
        m = re.match(r"(https?:\/\/)(.*):(\d*)(\/?.*)", self.routes[name])
        host = m.group(2)
        port = int(m.group(3))
        path = m.group(4)
        return host, port, path
