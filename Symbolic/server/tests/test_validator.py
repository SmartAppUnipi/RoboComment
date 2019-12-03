import pytest
from json_validator import Validator
import json

def test_position():
    with open('tests/dummy.json', 'r') as f: 
        dummy = json.load(f) 
    assert True == Validator.validate_positions(dummy[0])
    assert True == Validator.validate_positions(dummy[1])
    assert False == Validator.validate_positions(dummy[2])

def test_events():
    with open('tests/dummy.json', 'r') as f: 
        dummy = json.load(f) 
    assert False == Validator.validate_event(dummy[0])
    assert False == Validator.validate_event(dummy[1])
    assert True == Validator.validate_event(dummy[2])
