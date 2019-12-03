import unittest
import app as flaskapp
import json
import requests_mock
from utils.KnowledgeBase import KnowledgeBase

player1 = { "id" : 42,  "name" : "Ruicosta" }
player2 = { "id" : 7, "name" : "Ronaldo" }

team1 = { "id" : 42, "name" : "Napoli" }
team2 = { "id" : 7,  "name" : "Juventus" }

user1 = { "id" : 42, "favourite_team" : "Napoli" }

class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.KB_URL = flaskapp.KB_URL
        self.AUDIO_URL = flaskapp.AUDIO_URL

        flaskapp.app.config['TESTING'] = True
        self.client = flaskapp.app.test_client()
        

    def test_running_server(self):
        response = self.client.get("/api")

        assert response.status_code == 200
    
    def test_api_action1(self):
        ''' testing a basic flow of our application'''

        with open('CommentGenerator/tests/mock_assets/elementary/cross/input1.json', 'r') as json_file:
            input_json = json.load(json_file)

        with requests_mock.mock() as mock_request:
            mock_request.get(self.KB_URL + KnowledgeBase.TEAM + "/42", text=json.dumps(team1), status_code=200)
            mock_request.get(self.KB_URL + KnowledgeBase.TEAM + "/7", text=json.dumps(team2), status_code=200)
            mock_request.get(self.KB_URL + KnowledgeBase.USER + "/42", status_code=404)
            res = self.client.post("/api/action", data=json.dumps(input_json))

        assert res.status_code == 200
    
    def test_api_action2(self):
        ''' testing a basic flow of our application'''

        with open('CommentGenerator/tests/mock_assets/elementary/pass/input1.json', 'r') as json_file:
            input_json = json.load(json_file)

        with requests_mock.mock() as mock_request:
            mock_request.get(self.KB_URL + KnowledgeBase.PLAYER+ "/42", status_code=404)
            mock_request.get(self.KB_URL + KnowledgeBase.PLAYER + "/7", status_code=404)
            mock_request.get(self.KB_URL + KnowledgeBase.TEAM + "/42", text=json.dumps(team1), status_code=200)
            mock_request.get(self.KB_URL + KnowledgeBase.TEAM + "/7", text=json.dumps(team2), status_code=200)
            mock_request.get(self.KB_URL + KnowledgeBase.USER + "/42", status_code=404)
            res = self.client.post("/api/action", data=json.dumps(input_json))

        assert res.status_code == 200
    
    def test_api_action3(self):
        ''' testing a basic flow of our application'''

        with open('CommentGenerator/tests/mock_assets/elementary/shot/input1.json', 'r') as json_file:
            input_json = json.load(json_file)

        with requests_mock.mock() as mock_request:
            mock_request.get(self.KB_URL + KnowledgeBase.TEAM + "/42", text=json.dumps(team1), status_code=200)
            mock_request.get(self.KB_URL + KnowledgeBase.TEAM + "/7", text=json.dumps(team2), status_code=200)
            mock_request.get(self.KB_URL + KnowledgeBase.USER + "/42", text=json.dumps(user1), status_code=200)
            res = self.client.post("/api/action", data=json.dumps(input_json))

        assert res.status_code == 200