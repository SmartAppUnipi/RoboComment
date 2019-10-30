from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 

# Create your views here.
@csrf_exempt # avoid cross site request forgery checks
def index(request):
    if request.method == 'GET':
        return HttpResponse("Hello, nice GET")
    elif request.method == 'POST':
        return HttpResponse("Hello, nice POST")