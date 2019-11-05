import requests
import json


class SymbolicInterface:
    def __init__(self, host="127.0.0.1", port=3000):
        self.host = host
        self.port = port

    def send(self, timestamp, data: dict) -> int:
        """
        Send frame description
        :param timestamp: timestamp of current frame
        :param data: dictionary describing current situation
        :return: HTTP response code
        """
        endpoint = f"http://{self.host}:{self.port}/positions/{timestamp}"
        r = requests.post(url=endpoint, data=data)
        return r.status_code


if __name__ == "__main__":
    symbolic_interface = SymbolicInterface()

    with open("mocks/dummy.json", "r") as f:
        data = json.load(f)

    for x in data:
        code = symbolic_interface.send(0, x)
        assert code == 200
