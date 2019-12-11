

class MockKnowledgeBase():
    def __init__(self):
        pass

    def get_player(self, player_id):
        return "Player" + str(player_id)
    
    def get_team(self, team_id):
        return "Team" + str(team_id)
    
    def get_user_team(self,user_id):
        return "Team" + str(user_id)