import unittest
import json
from src.Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
from tests.MockKnowledgeBase import MockKnowledgeBase


class TestApi(unittest.TestCase):
    def setUp(self):
        self.kb = MockKnowledgeBase()
        self.commentator = Commentator(self.kb)       
       
    def test_run1(self):
        with open('CommentGenerator/tests/mock_assets/elementary/pass/input_symbolic1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        # checking if the output we pass to audio is well formed
        assert set(output.keys()) == set(['comment','emphasis','startTime','endTime','priority','id'])
        assert 0 <= output['priority'] and output['priority'] <= 5

    def test_run2(self):
        with open('CommentGenerator/tests/mock_assets/elementary/intercept/input_symbolic1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])
    
    def test_run3(self): 
        with open('CommentGenerator/tests/mock_assets/elementary/possession/input_symbolic1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])
    
    def test_run4(self): 
        with open('CommentGenerator/tests/mock_assets/elementary/pass/input_symbolic1.json', 'r') as json_file:
            input_json = json.load(json_file)
        
        output = self.commentator.run(input_json)

        print(output['comment'])
    

