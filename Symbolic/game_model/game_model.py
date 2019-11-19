import utils as utils
from stack import Stack

class GameModel:
    def __init__(self):
        self._ownership_stack = Stack()
        self._ownership_stack_last_update = 0
        self._ownership_stack.push_front(0)
        self._ownership_threshold = 2 # measured in meters
        self._vacant_since = None


    def update_stacks(self, new_data):
        # extract data from json
        ball_pos = new_data['ball'][0]
        pos = new_data['positions']
        time_ms = round(new_data['time'] * 1000)

        self._compute_new_owner(ball_pos, pos, time_ms)


    def _compute_new_owner(self, ball_pos, pos, time_ms): 
        # compute the closest player to the ball, 
        deltas = utils.deltaPlayersBall(pos)
        pot_owners = [a for a in deltas if a['distance'] < self._ownership_threshold]
        if self._vacant_since:
            if len(pot_owners) > 0:
                self._ownership_stack_last_update = time_ms
                new_owner = self._compute_closest_player(pot_owners)
                self._ownership_stack.push_front(new_owner)
                self._vacant_since = None
        else: 
            last_owner = self._ownership_stack.get(0)
            if not last_owner in [a['id'] for a in pot_owners]:
                self._ownership_stack_last_update = time_ms
                new_owner = self._compute_closest_player(pot_owners)
                self._ownership_stack.push_front(new_owner)
                if self._vacant_since:
                    self._ownership_stack_last_update = time_ms
                    self._ownership_stack.push_front(new_owner)
                    self._vacant_since = None


    def _compute_closest_player(self, pot_owners):
        closest = None
        dist = 1000
        for e in pot_owners:
            if e['distance'] < dist:
                closest = e['id']
                dist = e['distance']

        return closest
