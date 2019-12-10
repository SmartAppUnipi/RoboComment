from threading import Thread
from  multiprocessing import SimpleQueue
from .Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
import os
import json

class CommentatorPool:

    def __init__(self, kb_url, send_to_audio):
        self.kb_url = kb_url
        self.send_to_audio = send_to_audio
        self.commentator_pool = {}

        self._match_cache = {}
    
    def _new_commentator(self, match_id, symbolic_q, user_id, kb_url):
        print("Welcome to this match! I will be your commentator!")
        
        knowledge_base = KnowledgeBase(url= kb_url)
        commentator = Commentator(knowledge_base)

        #TODO here we need to start the state machine
        while True:
            event = symbolic_q.get()
            output = commentator.run(event)

            self.send_to_audio(output)

    def start_session(self,match_id, user_id ):
        session_status = 200 # session already present

        if match_id not in self.commentator_pool.keys():
            # adding a new key to the comentator pool
            # new session
            self.commentator_pool[match_id] = {}
            session_status = 201 

        
        if user_id in self.commentator_pool[match_id].keys():
            # the user session is already here
            return 200 # session already present

        symbolic_q = SimpleQueue()
        commentator = Thread(target=self._new_commentator,args=(match_id,symbolic_q,user_id, self.kb_url))

        self.commentator_pool[match_id][user_id] = {
            "symbolic_q" : symbolic_q,
            "commentator" : commentator
        }

        commentator.daemon = False
        commentator.start()

        return session_status
        
    def push_symbolic_event_to_match(self,match_id, event):
        if match_id not in self.commentator_pool.keys():
            return {}  

        self._cache_event(match_id,event)

        for user_id in self.commentator_pool[match_id]:
            self.commentator_pool[match_id][user_id]["symbolic_q"].put(event)

        return event
    
    def end_session(self,match_id,user_id):
        pass

    def _cache_event(self,match_id, event):
        if not os.path.isdir("./CommentGenerator/.match_cache"):
            os.mkdir("./CommentGenerator/.match_cache")
        
        if match_id not in  self._match_cache.keys():
            # new match
            self._match_cache[match_id] = []
        
        self._match_cache[match_id].append(event)

        # TODO need to figure out a way to implement this that is not time consuming



        
