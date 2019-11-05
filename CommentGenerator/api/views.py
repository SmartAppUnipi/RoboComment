from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 
import json
import requests

# Create your views here.
@csrf_exempt # avoid cross site request forgery checks
def action(request):
    if request.method == 'POST':
        action_json = json.loads(request.body)

        print(action_json)
        # main 
        
        # post to the audio group
        response = requests.post(url="http://127.0.0.1:8000/api/action/", data =json.dumps(action_json))
        return HttpResponse("Hello, nice POST")