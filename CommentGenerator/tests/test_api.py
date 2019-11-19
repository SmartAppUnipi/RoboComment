import unittest
import app as flaskapp
import json


class TestApi(unittest.TestCase):
    
    def setUp(self):
        flaskapp.app.config['TESTING'] = True
        self.client = flaskapp.app.test_client()
        

    def test_running_server(self):
        response = self.client.get("/api")

        assert response.status_code == 200
    
    def test_api_action1(self):
        ''' testing a basic flow of our application'''

        with open('tests/mock_assets/input1.json', 'r') as json_file:
            input_json = json.load(json_file)

        res = self.client.post("/api/action", data=json.dumps(input_json))

        assert res.status_code == 200