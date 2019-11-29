import unittest
import requests_mock
import json
from utils.KnowledgeBase import KnowledgeBase


class TestKnowledgeBase(unittest.TestCase):
    def setUp(self):
        self.KB_URL = "http://kbendpoint:4242/"
        self.kb = KnowledgeBase(self.KB_URL)

    def test_get_player1(self):

        player = {
	        "id": 42,
	        "name": "Nome Del Giocatore",
	        "club": "FC Crotone",
	        "height": "188",
	        "date_of_birth": "1992-09-29"
        }

        with requests_mock.mock() as mock_request:
            mock_request.get(self.KB_URL + self.kb.PLAYER + "/42", text=json.dumps(player), status_code=200)
            res = self.kb.get_player(42)

            assert res == "Nome Del Giocatore"
    
    def test_get_team1(self):

        team = {
	        "id": 42,
	        "country": "Italy",
	        "city": "Milano",
	        "name": "Nome Della Squadra"
        }

        with requests_mock.mock() as mock_request:
            mock_request.get(self.KB_URL + self.kb.TEAM + "/42", text=json.dumps(team), status_code=200)
            res = self.kb.get_team(42)

            assert res == "Nome Della Squadra"
    
    def test_get_team2(self):

        res = self.kb.get_team(42)

        assert res == "Team42"
    

    def test_get_match1(self):

        match = {
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

        with requests_mock.mock() as mock_request:
            mock_request.get(self.KB_URL + self.kb.MATCH +"/42", text=json.dumps(match), status_code=200)
            res = self.kb.get_match(42)

            assert res['home']['name'] == "SS Lazio"