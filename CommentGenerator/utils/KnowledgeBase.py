from pathlib import Path
import requests


class KnowledgeBase:

    player = 'persona'
    team = 'club'
    cup = 'cup'
    user = 'users'

    def __init__(self, url):
        self.url = Path(url)

    def get_player(self, player_id):
        return self.get_item(self.player, player_id)

    def get_team(self, team_id):
        return self.get_item(self.team, team_id)

    def get_cup(self, cup_id):
        return self.get_item(self.team, cup_id)

    def get_user(self, user_id):
        return self.get_item(self.team, user_id)

    def get_item(self, entity, id):
        resp = requests.get(self.url / entity / f':{id}')

        if resp.status_code == 200:
            return resp.json()  # Maybe we should check if the format is correct
        else:
            # TODO  Retun empty json without raising error so that the minimal pattern is matched (?)
            pass
