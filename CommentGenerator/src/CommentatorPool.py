from threading import Thread
from  multiprocessing import SimpleQueue
from .Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
import os
import json
import urllib
import time

class CommentatorPool:

    def __init__(self, kb_url, send_to_audio):
        self.kb_url = kb_url
        # upcall to send the produced output to the audio group
        self.send_to_audio = send_to_audio
        self.commentator_pool = {}

        # in memory cache, can be useful
        self.match_cache = SymbolicEventsCache()
    
    def _new_commentator(self, match_id, symbolic_q, user_id, kb_url):
        ''' this function is the body of the thread, there will be one thread per user'''
        run = True

        knowledge_base = KnowledgeBase(url= kb_url)
        commentator = Commentator(knowledge_base, user_id)

        while run:
            event = symbolic_q.get()

            if event:
                output = commentator.run(event)
                self.send_to_audio(output)
            else:
                # if the event is an empty json {} we stop that commentator
                run = False
    
    def _mock_symbolic_level(self, match_id, clip_uri):
        ''' this function is use to start a thread simulating the symbolic level when we already have the match in cache'''

        events = self.match_cache.get_events(match_id,clip_uri)

        for e in events:
            # wait some time before sending the next event to our module
            #TODO needs a smarter implementation
            time.sleep(2)
            self.push_symbolic_event_to_match(match_id,clip_uri,e, put_in_cache=False)

    def start_session(self, match_id, clip_uri, start_time, user_id ):
        '''
        starts a commentary for the user user_id, relative to the match match_id and clip_uri
        return True if the video is already in our cache
        '''
        # checking if we have the match in cache    
        in_cache = self.match_cache.in_cache(match_id,clip_uri)

        # just creating entries in our dict
        if match_id not in self.commentator_pool.keys():
            self.commentator_pool[match_id] = {}
        if clip_uri not in self.commentator_pool[match_id].keys():
            self.commentator_pool[match_id][clip_uri] = {}

        if user_id in self.commentator_pool[match_id][clip_uri].keys():
            # we already have an opened session for this user
            return True # in_cache should be true

        self.commentator_pool[match_id][clip_uri][user_id] = {}
        # symbolic q is used to push the symbolic events to the threads
        symbolic_q = SimpleQueue()
        commentator = Thread(target=self._new_commentator,args=(match_id,symbolic_q,user_id, self.kb_url))

        self.commentator_pool[match_id][clip_uri][user_id] = {
            "symbolic_mock" : None,
            "symbolic_q" : symbolic_q,
            "commentator" : commentator
        }

        # the threads will stop once the server is closed
        commentator.daemon = False
        commentator.start()

        if in_cache:
            # if we have the video in cache we simulate the symbolic level with a thread 
            # the thread will send our cached comments every tot seconds
            symbolic_mock = Thread(target=self._mock_symbolic_level,args=(match_id,clip_uri))
            self.commentator_pool[match_id][clip_uri][user_id]["symbolic_mock"] = symbolic_mock
            symbolic_mock.daemon = True
            symbolic_mock.start()
        # else
        # our thread is up and will wait for posts from the symbolic level

        return in_cache
        
    def end_session(self,user_id):
        ''' ends a commentary for the user user_id, relative to the match match_id'''
        # this is very expensive but the audio group is able to send only the user id to us
        for match_id in self.commentator_pool.keys():
            for clip_uri in self.commentator_pool[match_id].keys():
                # if the user has an active session
                if user_id  in self.commentator_pool[match_id][clip_uri].keys():
                    # closing the thread sending an empty json
                    self.commentator_pool[match_id][clip_uri][user_id]["symbolic_q"].put({})            
                    del self.commentator_pool[match_id][clip_uri][user_id]
                
                # else
                # if the user has no active session we do nothing
        return
        
    
    def push_symbolic_event_to_match(self,match_id, clip_uri, event, put_in_cache = True):

        if put_in_cache:
            self.match_cache.cache_event(match_id,clip_uri,event)

        if match_id not in self.commentator_pool.keys():
            return {}
        if clip_uri not in self.commentator_pool[match_id].keys():
            return {}  
        
        # for each user we send the event to the corresponding thread
        for user_id in self.commentator_pool[match_id][clip_uri]:
            self.commentator_pool[match_id][clip_uri][user_id]["symbolic_q"].put(event)

        return event    

        
class SymbolicEventsCache():
    def __init__(self):
        self.cache_path = "./CommentGenerator/.match_cache"
        self._check_and_mkdir(self.cache_path)
    

    def _check_and_mkdir(self,dirpath):
        already_present = os.path.isdir(dirpath)
        if not already_present:
            os.mkdir(dirpath)
        
        return already_present
    
    def _get_clip_path(self,match_id, clip_uri):
        clip_uri = urllib.parse.quote(clip_uri, safe='')

        return self.cache_path + "/" + str(match_id) + "/" + str(clip_uri)


    def in_cache(self, match_id, clip_uri):
        clip_path = self._get_clip_path(match_id,clip_uri)

        # ASSUME if the path exists that means we have cached the ENTIRE match
        return os.path.exists(clip_path)

    def cache_event(self,match_id, clip_uri, event):
        '''
        this function caches the json received from the symbolic level.
        for each match id there will be a directory
        in this dir there will be a directory per clip uri
        the a  file per input the name off the file is start_time end_time
        '''
        
        tmp_path = self.cache_path + "/" + str(match_id)
        self._check_and_mkdir(tmp_path)
        clip_path = self._get_clip_path(match_id,clip_uri)
        self._check_and_mkdir(clip_path)

        start_time = event['start_time']
        end_time = event['end_time']
        
        # ASSUME each event as unique start_time end_time 
        with open(clip_path + "/" + str(start_time) + "_" + str(end_time) + ".json","w+") as filejson:
            json.dump(event,filejson)

    
    def get_events(self,match_id,clip_uri):
        # returns a list of events
        symbolic_events = []

        clip_path = self._get_clip_path(match_id,clip_uri)

        for event_path in sorted(os.listdir(clip_path)):

            with open(clip_path + "/" + event_path,'r') as json_event:
                
                symbolic_events.append(json.load(json_event))
        
        return symbolic_events
    
    
    
