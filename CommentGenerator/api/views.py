from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 
import json
import requests


AUDIO_URL  = "http://10.101.12.139:5000"

# Create your views here.
@csrf_exempt # avoid cross site request forgery checks
def action(request):
    if request.method == 'POST':
        action_json = json.loads(request.body)

        print(action_json)
        # main 
        
        # post to the audio group
        response = requests.post(url=AUDIO_URL, data =json.dumps(action_json))
        return HttpResponse("Hello, nice POST")