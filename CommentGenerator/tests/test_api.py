import unittest
import app as flaskapp
import json
import shutil

assets = "CommentGenerator/tests/mock_assets/elementary/"
cache = "CommentGenerator/.match_cache"

io_json = {
    "match_id" : 42,
    "start_time" : 0,
    "match_url" : "http://clip.of.the.match/juve/napoli"
}


class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.KB_URL = flaskapp.KB_URL
        self.AUDIO_URL = flaskapp.AUDIO_URL

        flaskapp.app.config['TESTING'] = True
        self.client = flaskapp.app.test_client()

    def tear_down(self):
        ''' used to remove the cache'''
        shutil.rmtree(cache)

    def test_running_server(self):
        response = self.client.get("/api")
        assert response.status_code == 200

    def get_symbolic_intput(self, file_path):
        input_json = ""
        with open(assets + file_path, 'r') as json_file:
            input_json = json.load(json_file)
        return input_json

    def test_api_action1(self):
        ''' testing a basic flow of our application'''

        input_json = self.get_symbolic_intput('possession/input_symbolic1.json')

        print()
        # starting the session for match id 42 and user id 7
        self.client.post("/api/session/7", data=json.dumps(io_json))
        res = self.client.post("/api/action", data=json.dumps(input_json))
        res = self.client.post("/api/action", data=json.dumps(input_json))
        self.client.delete("/api/session/7")
            
        self.tear_down()
        assert res.status_code == 200
    
    def test_api_action2(self):
        ''' testing a basic flow of our application'''

        input_json = self.get_symbolic_intput('pass/input_symbolic1.json')
    
        # starting the session for match id 42 and user id 7
        self.client.post("/api/session/7", data=json.dumps(io_json))
        #res = self.client.post("/api/action", data=json.dumps(input_json))
        #res = self.client.post("/api/action", data=json.dumps(input_json))
        self.client.delete("/api/session/7")

       
    
    def test_api_action3(self):
        ''' testing a basic flow of our application'''

        input_json = self.get_symbolic_intput('intercept/input_symbolic1.json')

        # starting the session for match id 42 and user id 7
        self.client.post("/api/session/7", data=json.dumps(io_json))
        #res = self.client.post("/api/action", data=json.dumps(input_json))
        #res = self.client.post("/api/action", data=json.dumps(input_json))
        self.client.delete("/api/session/42/7")

        