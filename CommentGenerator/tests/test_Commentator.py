import unittest
import json
from src.Commentator import Commentator


class TestApi(unittest.TestCase):
    def setUp(self):
        self.commentator = Commentator()
       
    def test_run1(self):
        with open('tests/mock_assets/elementary/pass/input1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        # checking if the output we pass to audio is well formed
        assert set(output.keys()) == set(['comment','emphasis','startTime','endTime','priority'])
        assert 0 <= output['priority'] and output['priority'] <= 5

    def test_run2(self):
        with open('tests/mock_assets/elementary/cross/input1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])
    
    def test_run3(self):
        with open('tests/mock_assets/elementary/foul/input1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])
    
    def test_run4(self):
        with open('tests/mock_assets/elementary/move/input1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])
    
    def test_run5(self):
        with open('tests/mock_assets/elementary/possession/input1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])
    
    def test_run6(self):
        with open('tests/mock_assets/elementary/possession_lost/input1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])
    
    def test_run7(self):
        with open('tests/mock_assets/elementary/shot/input1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])