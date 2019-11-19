import unittest
import json
from src.Commentator import Commentator


class TestApi(unittest.TestCase):
    def setUp(self):
        self.commentator = Commentator()
       
    def test_run1(self):
        with open('tests/mock_assets/input1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        # checking if the output we pass to audio is well formed
        assert set(output.keys()) == set(['comment','emphasis','startTime','endTime','priority'])
        assert 0 <= output['priority'] and output['priority'] <= 5


 