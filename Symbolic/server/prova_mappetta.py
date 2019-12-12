import json 
import pprint
import random
import math
import time
import requests
import pprint
import json
import sys

pp = pprint.PrettyPrinter(indent=4)
url = "http://127.0.0.1:3001/positions"


with open('positions.json','r') as f:
    pos = json.load(f)
    i=0
    for p in pos:
        requests.post(url, json=p)
        time.sleep(0.1)