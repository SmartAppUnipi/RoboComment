from threading import Thread
from  multiprocessing import SimpleQueue
from .Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
import os
import json

class CommentatorPool:

    def __init__(self, kb_url, send_to_audio):
        self.kb_url = kb_url
        # upcall to send the produced output to the audio group
        self.send_to_audio = send_to_audio
        self.commentator_pool = {}

        # in memory cache, can be useful
        self._match_cache = {}
    
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

    def start_session(self,match_id, user_id ):
        ''' starts a commentary for the user user_id, relative to the match match_id'''
        session_status = 200 # session already present

        if match_id not in self.commentator_pool.keys():
            # adding a new key to the comentator pool
            self.commentator_pool[match_id] = {}
            session_status = 201 # new session

        
        if user_id in self.commentator_pool[match_id].keys():
            # the user session is already here
            return 200 # session already present

        # symbolic q is used to push the symbolic events to the threads
        symbolic_q = SimpleQueue()
        commentator = Thread(target=self._new_commentator,args=(match_id,symbolic_q,user_id, self.kb_url))

        self.commentator_pool[match_id][user_id] = {
            "symbolic_q" : symbolic_q,
            "commentator" : commentator
        }

        # the threads will stop once the server is closed
        commentator.daemon = True
        commentator.start()

        return session_status
        
    def end_session(self,match_id,user_id):
        ''' ends a commentary for the user user_id, relative to the match match_id'''
        # doing nothing if the match/user is not in commentary pool
        if match_id not in self.commentator_pool.keys():
            return
        if user_id not in self.commentator_pool[match_id].keys():
            return

        # closing the thread sending an empty json
        self.commentator_pool[match_id][user_id]["symbolic_q"].put({})
        # we now clean the commentator pool
        del self.commentator_pool[match_id][user_id]
        if not self.commentator_pool[match_id]:
            # user_id was the last user watching that game
            del self.commentator_pool[match_id]
        
    
    def push_symbolic_event_to_match(self,match_id, event):
        # caching the event, anyway
        self._cache_event(match_id,event)

        if match_id not in self.commentator_pool.keys():
            return {}  
        
        # for each user we send the event to the corresponding thread
        for user_id in self.commentator_pool[match_id]:
            self.commentator_pool[match_id][user_id]["symbolic_q"].put(event)

        return event    


    def _cache_event(self,match_id, event):
        '''
        this function caches the json received from the symbolic level.
        for each match id there will be a directory
        in this dir there will be a file per input 
        the name off the file is start_time end_time
        '''
        cache_path = "./CommentGenerator/.match_cache"
        if not os.path.isdir(cache_path):
            os.mkdir(cache_path)
        
        if match_id not in  self._match_cache.keys():
            # new match
            if not os.path.isdir(cache_path + "/" + str(match_id)):
                os.mkdir(cache_path + "/" + str(match_id))
            self._match_cache[match_id] = []
        
        self._match_cache[match_id].append(event)

        start_time = event['start_time']
        end_time = event['end_time']
        
        # ASSUME each event as unique start_time end_time 
        with open(cache_path + "/" + str(match_id) + "/" + str(start_time) + "_" + str(end_time) + ".json","w+") as filejson:
            json.dump(event,filejson)



        
