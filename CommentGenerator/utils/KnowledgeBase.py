import requests


class KnowledgeBase:

    def __init__(self, url):
        self.PLAYER = 'persona'
        self.TEAM = 'club'
        self.MATCH = 'cup'
        self.USER = 'users'

        # we keep the most recent player queried to reduce requests to the kb
        #TODO this can be extended keeping all the queries done
        self._saved_player = { "id" : -1,"name" : "undefined"}
        self._saved_team = { "id" : -1,"name" : "undefined"}

        self.url = url

    def get_player(self, player_id):
        ''' given a player id it returns his name'''

        if self._saved_player["id"] != player_id:
            self._saved_player = self.get_item(self.PLAYER, player_id)
        
        return self._saved_player["name"]

    def get_team(self, team_id):
        ''' given a team id it returns his name '''
        
        if self._saved_team["id"] != team_id:
            self._saved_team = self.get_item(self.TEAM, team_id)
        
        return self._saved_team["name"]

    def get_match(self, match_id):
        return self.get_item(self.MATCH, match_id)

    def get_user(self, user_id):
        return self.get_item(self.USER, user_id)

    def get_item(self, entity, id):
        try:
            resp = requests.get( self.url + entity + "/" + str(id))
        except requests.exceptions.ConnectionError:
            return {"id" : -1, "name" : "undefined"}

        if resp.status_code == 200:
            return resp.json()  # Maybe we should check if the format is correct
        else:
            return {"id" : -1, "name" : "undefined"}
