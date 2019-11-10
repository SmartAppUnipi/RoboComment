from game_model.symbolic_stack import RegexStack

class GameView:
    def __init__(self, matcher):
        self._stacks = [] # list of stacks
        self._stacks.append((RegexStack, 0)) # 0 stands for last modified now
        # self._full_game = (RegexStack, 0) # full game log

    def update_stacks(self, current_situation):
        for s in self._stacks:
            pass