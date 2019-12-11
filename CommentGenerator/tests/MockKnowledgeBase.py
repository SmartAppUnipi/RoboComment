

class MockKB():
    def __init__(self):
        pass

    def get_player(self, player_id):
        return "Player" + str(player_id)
    
    def get_team(self, team_id):
        return "Team" + str(team_id)
    
    def get_user_team(self,user_id):
        return 42

    def get_user_player(self,user_it):
        return 7