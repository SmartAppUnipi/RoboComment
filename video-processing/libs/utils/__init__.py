import re

class ServerArgs(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def get_team_numbers_from_kb(kb_json_response):
    numbers = set()
    for p1, p2 in zip(kb_json_response['home_team'], kb_json_response['away_team']):
        # numbers.add(int(p1['number']))
        numbers.add(int(re.sub('[^0-9]','', p1['number'])))
        numbers.add(int(re.sub('[^0-9]','', p2['number'])))
        # numbers.add(int(p2['number']))

    # add substitute players numbers since they're not provided
    for n in [21, 30, 23, 16, 95, 8, 19, 9, 21, 31]:
        numbers.add(n)

    return list(numbers)