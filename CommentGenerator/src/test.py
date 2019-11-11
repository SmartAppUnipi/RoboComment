import requests
import json

#Simulazione Symbolic Level
if __name__ == '__main__':
    with open('../assets/input1.json', 'r') as json_file:
        input = json.load(json_file)
    res = requests.post(url="http://127.0.0.1:5555/api/action", json=input)
    print(res.text)