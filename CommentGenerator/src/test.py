import requests
import json

#Simulazione Symbolic Level
if __name__ == '__main__':
    # with open('../assets/input1.json', 'r') as json_file:
    #     input = json.load(json_file)
    # res = requests.post(url="http://127.0.0.1:5555/api/action", json=input)
    # print(res.text)

    event = {
        'player1': 'Sportiello',
        'player2': '{player2}'
    }

    with open('../assets/prova.txt', 'r') as file:
        str = file.readline()
        str = str.format(**event)
        print(str.format(player2='Maradona'))
