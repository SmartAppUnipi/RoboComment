

class MockKB():
    def __init__(self):
        self.data = {
            "players" : {   
                42 : "Ronaldo",
                41 : "Bernardeschi",
                7 : "Koulibaly"
            },
            "teams" : {
                42 : "Juventus",
                7 : "Napoli",
                5 : "Inter"
            },
            "match" : {
                42 :  {
                "home": {
                    "id": 3162,
                    "name": "SS Lazio"
                },
                "away": {
                    "id": 3161,
                    "name": "FC Internazionale Milano"
                },
                "result": ["2", "3"],
                "home_team": [{
                    "id": "130",
                    "name": "S. de Vrij",
                    "club": 3162,
                    "role": "Defender"
                }],
                "away_team": [{
                    "id": "21094",
                    "name": "D. D'Ambrosio",
                    "club": 3161,
                    "role": "Defender"
                }]
        }
            }
        }

    def get_player(self, player_id):
        return self.data['players'][player_id]
    
    def get_team(self, team_id):
        return self.data['teams'][team_id]
    def get_role_player(self,match_id, player_id):
        return "defender"
    
    def get_user_team(self,user_id):
        return self.data['teams'][42]

    def get_user_player(self,user_id):
        return self.data['players'][42]
    
    def get_user_language(self,user_id):
        return 'en'