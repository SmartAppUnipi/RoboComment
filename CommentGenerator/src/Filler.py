

class Filler:

    def __init__(self, config=None):
        if config is not None:
            self._load_config(config)

    def update_comment(self, comment, details):
        main_actor = details["player1"]
        
        return comment.format(player1=main_actor, modifier="fantastic")

    def _load_config(self,config):
        return None