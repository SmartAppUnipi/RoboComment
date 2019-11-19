from ElementaryBlock import ElementaryBlock
from player import player

class PassBlock(ElementaryBlock):
    def __init__(self, first, second):
        if type(first) is not player:
            raise TypeError
        #First is type player
        if type(first)is not type(second):
            raise TypeError
        #Both are type player
        if first.team != second.team:
            pass
            #ToDo raise WrongTeamException
        self.from_player=first
        self.to_player=second