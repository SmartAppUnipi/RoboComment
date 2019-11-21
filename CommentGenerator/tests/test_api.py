import unittest
import app as flaskapp
import json
import requests_mock
from pathlib import Path

class TestApi(unittest.TestCase):
    
    def setUp(self):
        flaskapp.app.config['TESTING'] = True
        self.client = flaskapp.app.test_client()
        

    def test_running_server(self):
        response = self.client.get("/api")

        assert response.status_code == 200
    
    def test_api_action1(self):
        ''' testing a basic flow of our application'''
        audio_module_input = {}

        def audio_module(request,context):
            # this function will mock the audio module 
            # it stores the json we send to the audio
            nonlocal audio_module_input
            audio_module_input = json.loads(request.body)

        with open(Path('CommentGenerator/tests/mock_assets/input1.json'), 'r') as json_file:
            input_json = json.load(json_file)

        with requests_mock.mock() as mock_request:
            # notifying the mock manager to care about a particular post request
            # x.x.x.x is the default value used to init AUDIO IP 
            mock_request.post("http://x.x.x.x:3003/", text=audio_module, status_code=200)
            res = self.client.post("/api/action", data=json.dumps(input_json))

        # checking if the json we send to audio is well formed

        assert set(audio_module_input.keys()) == set(['comment','emphasis','startTime','endTime','priority'])
        assert audio_module_input['priority'] >= 0 and audio_module_input['priority'] <= 5