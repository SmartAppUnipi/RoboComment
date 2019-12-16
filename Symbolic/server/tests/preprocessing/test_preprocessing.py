from game_model.game_model import GameModel

game_model = GameModel()

def test_1():

    input_ = open("tests/preprocessing/rules_input.txt", "r").readlines()
    target = open("tests/preprocessing/rules_target.txt", "r").readlines()

    for r, target in zip(input_, target):
        if r == "":
            continue

        rule = game_model._pythonize_rule(r)
        assert rule == target
