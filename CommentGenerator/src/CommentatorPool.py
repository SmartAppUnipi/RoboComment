from threading import Thread
from  multiprocessing import SimpleQueue
from .Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
import os
import json
import urllib
import time
import logging

class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

def is_an_action(event):
    '''
        given a json object from the symbolic group returns True if is an object describing 
        the action on the field, returns False otherwise (if it is a position)
    '''
    return 'type' in event.keys() and event['type'] != "positions"

def is_a_position(event):
    return 'type' in event.keys() and event['type'] == "positions"

class CommentatorPool:

    def __init__(self, kb_url, send_to_audio):
        self.kb_url = kb_url
        # upcall to send the produced output to the audio group
        self.send_to_audio = send_to_audio
        self.commentator_pool = {}

        # in memory cache, can be useful
        self.match_cache = SymbolicEventsCache()
    
    def _new_commentator(self, match_id, symbolic_q, user_id, kb_url):
        ''' this function is the body of the commentator thread, there will be one thread per user'''
        run = True

        knowledge_base = KnowledgeBase(url= kb_url)
        commentator = Commentator(knowledge_base, user_id, match_id)

        while run:
            event = symbolic_q.get()

            if event:
                print("INPUT:: " + str(event))
                logging.info(input)

                output = commentator.run(event)
                self.send_to_audio(output)
                
                print(bcolors.OKGREEN + "OUTPUT:: " + output['comment'] + bcolors.ENDC)
                logging.info(output)
            else:
                # if the event is an empty json {} we stop that commentator
                run = False
    
    def symbolic_mock(self, match_id, clip_uri):
        ''' this function is use to start a thread simulating the symbolic level when we already have the match in cache'''
        for a in self.match_cache.get_next_action(match_id,clip_uri):
            # wait some time before sending the next action to our module
            self.dispatch_event(match_id,clip_uri, a)

            # we wait 50% of the action time, then we send another action
            # this just a trivial implementation to avoid sending all the comments at once
            sleep_time = (a['end_time'] - a['start_time']) / 2
            time.sleep(sleep_time)

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
            return in_cache

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
            symbolic_mock = Thread(target=self.symbolic_mock ,args=(match_id,clip_uri))
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
    
    
    def dispatch_event(self,match_id, clip_uri, event):
        if match_id not in self.commentator_pool.keys():
            return {}
        if clip_uri not in self.commentator_pool[match_id].keys():
            return {}  
        
        # for each user we send the event to the corresponding thread
        for user_id in self.commentator_pool[match_id][clip_uri]:
            if is_an_action(event):
                # the action can be used to produce a comment
                self.commentator_pool[match_id][clip_uri][user_id]["symbolic_q"].put(event)
            elif is_a_position(event):
                # the event is a position
                self.send_to_audio(event)

        return event   

    def cache(self, match_id, clip_uri, event):
        self.match_cache.cache_event(match_id, clip_uri, event) 



        
class SymbolicEventsCache():
    def __init__(self):
        self.cache_path = "CommentGenerator/.match_cache"
        self._check_and_mkdir(self.cache_path)
    

    def _check_and_mkdir(self,dirpath):
        already_present = os.path.isdir(dirpath)
        if not already_present:
            os.mkdir(dirpath)
        
        return already_present
    
    def get_clip_path(self,match_id, clip_uri):
        clip_uri = urllib.parse.quote(clip_uri, safe='')

        return self.cache_path + "/" + str(match_id) + "/" + str(clip_uri)


    def in_cache(self, match_id, clip_uri):
        clip_path = self.get_clip_path(match_id,clip_uri)

        # ASSUME if the path exists that means we have cached the ENTIRE match
        return os.path.exists(clip_path)

    def cache_event(self,match_id, clip_uri, event):
        match_path = self.cache_path + "/" + str(match_id)
        clip_path = self.get_clip_path(match_id,clip_uri)

        self._check_and_mkdir(match_path)
        self._check_and_mkdir(clip_path)

        if is_a_position(event) or is_an_action(event):
            
            if is_a_position(event):
                etype = 'positions'
            else:
                etype = 'actions'
            
            event_file = open(clip_path + '/' + etype, 'a+')
            dumped_event = json.dumps(event)
            event_file.write(dumped_event + " \n")
            event_file.close()



    def _get_events(self, match_id, clip_uri, etype):
        clip_path = self.get_clip_path(match_id,clip_uri)

        event_file = open(clip_path + '/' + etype, 'r')
        events = event_file.read()  
        event_file.close()

        return events

    def get_next_action(self,match_id,clip_uri):
        actions = self._get_events(match_id,clip_uri,'actions')

        for line in actions.splitlines():

            yield json.loads(line)

    
    def get_next_position(self, match_id, clip_uri):
        pass

    
    
