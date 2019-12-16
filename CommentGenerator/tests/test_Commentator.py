import unittest
import json
from src.Commentator import Commentator
from utils.KnowledgeBase import KnowledgeBase
from tests.MockKnowledgeBase import MockKB


class TestCommentator(unittest.TestCase):
    def setUp(self):
        self.kb = MockKB()
        self.commentator = Commentator(self.kb, user_id=7)

        self.duel_input = self.get_symbolic_intput('duel/input_symbolic1.json')
        self.goal_input = self.get_symbolic_intput('goal/input_symbolic1.json')
        self.intercept_input = self.get_symbolic_intput('intercept/input_symbolic1.json')
        self.offside_input = self.get_symbolic_intput('offside/input_symbolic1.json')
        self.pass_input = self.get_symbolic_intput('pass/input_symbolic1.json')
        self.penalty_input = self.get_symbolic_intput('penalty/input_symbolic1.json')
        self.possession_input = self.get_symbolic_intput('possession/input_symbolic1.json')
        self.revoked_goal_input = self.get_symbolic_intput('revoked_goal/input_symbolic1.json')
        self.shot_off_target = self.get_symbolic_intput('shot_off_target/input_symbolic1.json')
        self.shot_on_target = self.get_symbolic_intput('shot_on_target/input_symbolic1.json')
        self.tikitaka = self.get_symbolic_intput('tikitaka/input_symbolic1.json')

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

    def test_run5(self):
        self.skip_welcome_message()

        output = self.commentator.run(self.duel_input)

        print(output['comment'])

    def test_run6(self):
        self.skip_welcome_message()

        output = self.commentator.run(self.shot_off_target)

        print(output['comment'])

    def test_run7(self):
        self.skip_welcome_message()

        output = self.commentator.run(self.shot_on_target)

        print(output['comment'])

    def test_run8(self):
        self.skip_welcome_message()

        output = self.commentator.run(self.tikitaka)

        print(output['comment'])

    def test_run9(self):
        self.skip_welcome_message()

        output = self.commentator.run(self.revoked_goal_input)

        print(output['comment'])

    def test_run10(self):
        self.skip_welcome_message()

        output = self.commentator.run(self.goal_input)

        print(output['comment'])

    def test_run11(self):
        self.skip_welcome_message()

        output = self.commentator.run(self.offside_input)

        print(output['comment'])

    def test_run12(self):
        self.skip_welcome_message()

        output = self.commentator.run(self.penalty_input)

        print(output['comment'])