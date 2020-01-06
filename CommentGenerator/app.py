import nltk
from flask import Flask, request
import json
import requests
import sys
from src.CommentatorPool import CommentatorPool
from utils.KnowledgeBase import KnowledgeBase
from threading import Thread
import logging

app = Flask(__name__)

AUDIO_URL = "http://audio.url:3003/"
KB_URL = "http://kb.url:3004/"
commentator_pool = None

@app.route('/api', methods=['GET'])
def api():
    ''' this interface can be used to check if the server is up and running '''
    return "Hi! the server is alive!"


def send_to_audio(output):
    ''' this function will send our output to the audio'''
    headers = {'Content-type': 'application/json'}
    try:
        requests.post(url=AUDIO_URL, json=output, headers=headers)
    except requests.exceptions.ConnectionError:
        print("Audio unreachable at " + AUDIO_URL)


# the endpoint will still be /api/action to avoid endless tuning with other groups
# the name action is no more significative since we get also positions here
@app.route('/api/action', methods=['POST'])
def events():
    ''' 
        it gets a json from the symbolic group, and forwards it to the right commentator
    '''
    global commentator_pool

    event = json.loads(request.data)

    response = ("OK", 200)
    # the input MUST have the match_id and the clip_uri
    if "match_id" in event.keys() and "match_url" in event.keys():
        match_id = event["match_id"]
        clip_uri = event["match_url"]
        
        logging.info(event)
        commentator_pool.cache(match_id, clip_uri, event)
        commentator_pool.dispatch_event(match_id, clip_uri , event) 
    else:
        print("BAD REQUEST from symbolic")
        response = ("BAD REQUEST",400)

    return response

@app.route('/api/session/<int:userid>', methods=['POST'])
def session_start(userid):
    ''' this method will be called by the audio each time a new user watches a match'''
    global commentator_pool
    
    video_json = json.loads(request.data)
    match_id = video_json['match_id']
    start_time = video_json['start_time']
    clip_uri = video_json['match_url']
    print("CLIP_URI " + clip_uri)

    in_cache = commentator_pool.start_session(match_id,clip_uri, start_time, userid)

    return "OK", 200 if in_cache else 201

@app.route('/api/session/<int:userid>', methods=['DELETE'])
def session_end(userid):
    ''' this method will be called by the audio each time a user ends the video streaming'''
    global commentator_pool

    commentator_pool.end_session(userid)
    return "OK"


@app.before_first_request
def init():
    ''' this function will be called at the application startup to initialize our module '''
    global commentator_pool
    # store lexicon
    nltk.download('vader_lexicon')

    logging.basicConfig(filename='CommentGenerator/commentgenerator.log',level=logging.INFO) # filemode='w'

    commentator_pool = CommentatorPool(KB_URL, send_to_audio)

if __name__ == '__main__':
    try:
        with open("routes.json",'r') as servicesfile:
            services = json.load(servicesfile)
            AUDIO_URL = services['fabula']
            KB_URL = services['qi']
    
    except FileNotFoundError:
        print("No routes.json file provided")
    
    app.run(host='0.0.0.0', port=3002)
