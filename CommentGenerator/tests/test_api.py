import unittest
import app as flaskapp
import json
import shutil
import os
import time

assets = "CommentGenerator/tests/mock_assets/elementary/"
cache = "CommentGenerator/.match_cache/"

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
        flaskapp.init()

        self.goal_input = self.get_symbolic_intput('goal/input_symbolic1.json')
        self.pass_input = self.get_symbolic_intput('pass/input_symbolic1.json')
        self.possession_input = self.get_symbolic_intput('possession/input_symbolic1.json')
        self.intercept_input = self.get_symbolic_intput('intercept/input_symbolic1.json')

        print()
    
    def tearDown(self):
        shutil.rmtree(cache)
        return

    def test_running_server(self):
        response = self.client.get("/api")
        assert response.status_code == 200

    def get_symbolic_intput(self, file_path):
        input_json = ""
        with open(assets + file_path, 'r') as json_file:
            input_json = json.load(json_file)
        return json.dumps(input_json) # this is quite hugly

    def test_api_action1(self):        
        # starting the session for match id 42 and user id 7
        self.client.post("/api/session/7", data=json.dumps(io_json))
        # the first message will produce a welcome comment
        res = self.client.post("/api/action", data = self.pass_input)
        res = self.client.post("/api/action", data = self.pass_input)
        res = self.client.post("/api/action", data = self.intercept_input)
        res = self.client.post("/api/action", data = self.possession_input)
        self.client.delete("/api/session/7")
            
        assert res.status_code == 200
    
    def test_api_action2(self):
        res = self.client.post("/api/action", data = json.dumps({"nomatchid" : "noclipuri"}))
        assert res.status_code == 400
       
    
    def api_action3(self):
        res1 = self.client.post("/api/session/7", data=json.dumps(io_json))   
        self.client.post("/api/action", data = self.pass_input)
        res2 = self.client.post("/api/session/8", data=json.dumps(io_json))

        self.client.delete("/api/session/7")
        self.client.delete("/api/session/8")
        
        assert res1.status_code == 201
        assert res2.status_code == 200
    
    def test_api_positions(self):
        iterations = 1000
        start_time = time.time()
        for i in range(iterations):
            self.client.post("/api/action", data = json.dumps({'match_id' : 42, 'match_url' : 'http://match.url/', 'type':'positions'}))
            
        elapsed_time = (time.time() - start_time)/iterations
        print(elapsed_time)
        assert elapsed_time < 0.3