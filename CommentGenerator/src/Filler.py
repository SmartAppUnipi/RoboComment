

class Filler:

    def __init__(self, config=None):
        if config is not None:
            self._load_config(config)

    def update_comment(self, comment, details):
        main_actor = details["player1"]
        team1 = details["team1"]
        field_zone = details["field_zone"]
        second_actor = details["player2"]
        
        return comment.format(player1=main_actor, team1=team1, field_zone=field_zone, player2=second_actor)

    def _load_config(self,config):
        return None