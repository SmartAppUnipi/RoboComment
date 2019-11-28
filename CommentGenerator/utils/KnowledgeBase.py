import requests


class KnowledgeBase:

    def __init__(self, url):
        self.player = 'persona'
        self.team = 'club'
        self.match = 'cup'
        self.user = 'users'

        self.url = url

    def get_player(self, player_id):
        return self.get_item(self.player, player_id)

    def get_team(self, team_id):
        return self.get_item(self.team, team_id)

    def get_match(self, match_id):
        return self.get_item(self.match, match_id)

    def get_user(self, user_id):
        return self.get_item(self.user, user_id)

    def get_item(self, entity, id):
        resp = requests.get( self.url + entity + "/" + str(id))

        if resp.status_code == 200:
            return resp.json()  # Maybe we should check if the format is correct
        else:
            return {}
