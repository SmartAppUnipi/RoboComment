import json

class SentimentUpdater():

    def add_emphasis(self, updated_comment): #TODO change name
        # start and end
        # importante che l'audio sappia la finestra temporale a cui corrisponde il commneto
        comment_json = {
            "comment" : updated_comment,
            "emphasis" : 15,
            "timestart" : "11.30", 
            "timeend" : "11.40",
            "priority" : 0.5
            
        }
        return  json.dumps(comment_json) 