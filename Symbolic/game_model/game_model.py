import game_model.utils as utils
from game_model.stack import Stack

class GameModel:
    def __init__(self):
        self._ownership_stack = (Stack(), 0)
        self._ownership_threshold = 2


    def update_stacks(self, positions):
        ball_pos = positions['ball'][0]
        pos = positions['positions']
        pot_owner = [a for a in utils.deltaPlayersBall(pos) if a['distance'] < self._ownership_threshold]
        
