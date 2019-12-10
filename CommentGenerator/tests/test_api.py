import unittest
import app as flaskapp
import json
import requests_mock
from utils.KnowledgeBase import KnowledgeBase

assets = "CommentGenerator/tests/mock_assets/elementary/"

player1 = { "id" : 42,  "name" : "Koulibaly" }
player3 = { "id" : 41,  "name" : "Di Lorenzo" }
player2 = { "id" : 7, "name" : "Ronaldo" }

team1 = { "id" : 42, "name" : "Napoli" }
team2 = { "id" : 7,  "name" : "Juventus" }

user1 = { "id" : 10, "favourite_team" : "Napoli" }

class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.KB_URL = flaskapp.KB_URL
        self.AUDIO_URL = flaskapp.AUDIO_URL

        flaskapp.app.config['TESTING'] = True
        self.client = flaskapp.app.test_client()
    

    def _mock_requests(self,mock):
        mock.get(self.KB_URL + KnowledgeBase.PLAYER+ "/42", text=json.dumps(player1),  status_code=200)
        mock.get(self.KB_URL + KnowledgeBase.PLAYER+ "/41", text=json.dumps(player3),  status_code=200)
        mock.get(self.KB_URL + KnowledgeBase.PLAYER + "/7", text=json.dumps(player2), status_code=200)
        mock.get(self.KB_URL + KnowledgeBase.TEAM + "/42", text=json.dumps(team1), status_code=200)
        mock.get(self.KB_URL + KnowledgeBase.TEAM + "/7", text=json.dumps(team2), status_code=200)
        mock.get(self.KB_URL + KnowledgeBase.USER + "/10", text=json.dumps(user1), status_code=200)

        mock.post(self.AUDIO_URL, status_code=200)

    def test_running_server(self):
        response = self.client.get("/api")

        assert response.status_code == 200
    
    def test_api_action1(self):
        ''' testing a basic flow of our application'''

        with open(assets + 'possession/input_symbolic1.json', 'r') as json_file:
            input_json = json.load(json_file)

        with requests_mock.mock() as mock_request:
            self._mock_requests(mock_request)
            print()
            # starting the session for match id 42 and user id 7
            self.client.post("/api/session/start/42/7")
            res = self.client.post("/api/action", data=json.dumps(input_json))

        assert res.status_code == 200
    
    def test_api_action2(self):
        ''' testing a basic flow of our application'''

        with open(assets + 'pass/input_symbolic1.json', 'r') as json_file:
            input_json = json.load(json_file)

        with requests_mock.mock() as mock_request:
            self._mock_requests(mock_request)
            print()
            # starting the session for match id 42 and user id 7
            self.client.post("/api/session/start/42/7")
            res = self.client.post("/api/action", data=json.dumps(input_json))

        assert res.status_code == 200
    
    def test_api_action3(self):
        ''' testing a basic flow of our application'''

        with open(assets + 'intercept/input_symbolic1.json', 'r') as json_file:
            input_json = json.load(json_file)

        with requests_mock.mock() as mock_request:
            self._mock_requests(mock_request)
            print()
            # starting the session for match id 42 and user id 7
            self.client.post("/api/session/start/42/7")
            res = self.client.post("/api/action", data=json.dumps(input_json))

        assert res.status_code == 200