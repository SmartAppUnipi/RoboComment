from game_model.symbolic_stack import RegexStack

class GameView:
    def __init__(self, matcher):
        self._stacks = [] # list of stacks
        self._stacks.append((RegexStack, 0)) # 0 stands for last modified now
        # self._full_game = (RegexStack, 0) # full game log
        self._previous_owner = None
        self._current_owner = None
        self._ball_vacancy_time = 0

    def update_stacks(self, positions, timestamp):
        ball_pos = positions['ball'][0]
        for s in self._stacks:
            pass

    def compute_owner(self, positions):
        for 