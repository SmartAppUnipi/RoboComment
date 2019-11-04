import json

class SentimentUpdater():

    def add_emphasis(self, updated_comment): #TODO change name

        comment_json = {
            "comment" : updated_comment,
            "emphasis" : 15
        }
        return  json.dumps(comment_json)