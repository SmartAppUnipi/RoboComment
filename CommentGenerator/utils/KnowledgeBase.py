import requests

# TODO add querying about favourite player
# TODO add queryng about info of particular id

class KnowledgeBase:
    PLAYER = 'persona'
    TEAM = 'club'
    MATCH = 'cup'
    USER = 'users'

    def __init__(self, url):
        # we keep the most recent player queried to reduce requests to the kb
        #TODO this can be extended keeping all the queries done
        self._saved_player = { "id" : -1}
        self._saved_team = { "id" : -1}

        self.url = url

    def get_player(self, player_id):
        ''' given a player id it returns his name'''

        if self._saved_player["id"] != player_id:
            tmp_player =  self.get_item(KnowledgeBase.PLAYER, player_id)
            self._saved_player = tmp_player if tmp_player else { "id" : -1,"name" : "Player" + str(player_id)}
        
        return self._saved_player["name"]

    def get_team(self, team_id):
        ''' given a team id it returns his name '''
        if self._saved_team["id"] != team_id:
            tmp_team = self.get_item(KnowledgeBase.TEAM, team_id)
            self._saved_team = tmp_team if tmp_team else { "id" : -1,"name" : "Team" + str(team_id)}
        
        return self._saved_team["name"]

    def get_match(self, match_id):
        return self.get_item(KnowledgeBase.MATCH, match_id)

    def get_user_team(self, user_id):
        tmp_user = self.get_item(KnowledgeBase.USER, user_id)
        return tmp_user['favourite_team'] if tmp_user else " "
    
    def get_user_player(self,user_id):
        tmp_user = self.get_item(KnowledgeBase.USER, user_id)
        return tmp_user['favourite_player'] if tmp_user else " "
    
    def get_user_language(self,user_id):
        tmp_user = self.get_item(KnowledgeBase.USER, user_id)
        return tmp_user['language'] if tmp_user else "en"
    
    def get_item(self, entity, id):
        try:
            resp = requests.get( self.url + entity + "/" + str(id))
        except requests.exceptions.ConnectionError:
            return {}

        if resp.status_code == 200:
            return resp.json()  # Maybe we should check if the format is correct
        else:
            return {}
