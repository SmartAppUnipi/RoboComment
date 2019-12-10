from threading import Thread
from  multiprocessing import SimpleQueue
from .Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase


class CommentatorPool:

    def __init__(self, kb_url, send_to_audio):
        self.kb_url = kb_url
        self.send_to_audio = send_to_audio
        self.commentator_pool = {}
    
    def _new_commentator(self,match_id, symbolic_q, user_q, kb_url):
        print("Welcome to this match! I will be your commentator!")
        
        knowledge_base = KnowledgeBase(url= kb_url)
        commentator = Commentator(knowledge_base)

        #TODO here we need to start the state machine
        while True:
            event = symbolic_q.get()
            output = commentator.run(event)
            
            self.send_to_audio(output)

    def comment_match(self,match_id):
        if match_id in self.commentator_pool.keys():
            return

        symbolic_q = SimpleQueue()
        user_q = SimpleQueue()
        commentator = Thread(target=self._new_commentator,args=(match_id,symbolic_q,user_q, self.kb_url))

        self.commentator_pool[match_id] = {
            "symbolic_q" : symbolic_q,
            "commentator" : commentator,
            "user_q" : user_q 
        }
        commentator.daemon = True
        commentator.start()

        return
    
    def add_user_to_match(self,match_id, user_id):
        if match_id not in self.commentator_pool.keys():
            return  -1
        
        self.commentator_pool[match_id]["user_q"].put(user_id)
        return user_id
    
    def push_symbolic_event_to_match(self,match_id, event):
        if match_id not in self.commentator_pool.keys():
            return {}  

        self.commentator_pool[match_id]["symbolic_q"].put(event)
        return event