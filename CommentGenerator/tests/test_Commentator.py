import unittest
import json
from src.Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
from tests.MockKnowledgeBase import MockKB


class TestCommentator(unittest.TestCase):
    def setUp(self):
        self.kb = MockKB()
        self.commentator = Commentator(self.kb, user_id=7)       

        self.goal_input = self.get_symbolic_intput('goal/input_symbolic1.json')
        self.pass_input = self.get_symbolic_intput('pass/input_symbolic1.json')
        self.possession_input = self.get_symbolic_intput('possession/input_symbolic1.json')
        self.intercept_input = self.get_symbolic_intput('intercept/input_symbolic1.json')
    
    def get_symbolic_intput(self, file_path):
        assets = "CommentGenerator/tests/mock_assets/elementary/"
        input_json = ""
        with open(assets + file_path, 'r') as json_file:
            input_json = json.load(json_file)
        return input_json # this is quite hugly
       
    def skip_welcome_message(self):
        self.commentator.run({"start_time" : 0, "end_time" : 1})

    def test_output_format(self):        
        output = self.commentator.run(self.pass_input)

        # checking if the output we pass to audio is well formed
        assert set(output.keys()) == set(['comment','emphasis','startTime','endTime','priority','id','language','voice'])
        assert 0 <= output['priority'] and output['priority'] <= 5

    def test_run2(self):
        self.skip_welcome_message()
        
        output = self.commentator.run(self.intercept_input)

        print(output['comment'])
    
    def test_run3(self): 
        self.skip_welcome_message()
        
        output = self.commentator.run(self.possession_input)

        print(output['comment'])
    
    def test_run4(self): 
        self.skip_welcome_message()
        
        output = self.commentator.run(self.pass_input)

        print(output['comment'])
    

