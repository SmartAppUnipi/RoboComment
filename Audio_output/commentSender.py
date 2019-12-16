import json
import requests
import time

serverURL = 'http://localhost:3003/'

headers = {
    'Content-type': 'application/json',
}

with open('comments.json') as json_file:
    json_data = json.load(json_file)
    print(json_data)
    for comment in json_data['comments']:
#         time.sleep(1)
        print(comment)
        r = requests.post(serverURL, data=json.dumps(comment), headers=headers)
