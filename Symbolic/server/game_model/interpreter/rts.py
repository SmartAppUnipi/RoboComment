from game_model.game_model import GameModel
import re

def _resolve_placeholders(s):
    for param in re.findall(r'@\d', s):
        s = s.replace(
            param, "registers['{}']".format(param)
        )
    return s

def check(constraints):
    if len(constraints) < 1:
        return True
    constraints_prime = _resolve_placeholders(constraints)
    registers = GameModel.get_env()['registers']
    return eval(constraints_prime)

def fire(actions):
    actions_prime = _resolve_placeholders(actions)
    stacks = GameModel.get_env()['stacks']
    registers = GameModel.get_env()['registers']
    eval(actions_prime)

def push(stack, element):
    print("=================================================")
    stacks = GameModel.get_env()['stacks']
    stacks[stack].append(element)

def spacchetpush(stack, element):
    registers = GameModel.get_env()['registers']
    push(stack, registers[element])