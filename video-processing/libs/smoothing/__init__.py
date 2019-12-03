import numpy as np
from libs.entity_tracker.sort import KalmanBoxTracker
from .motion import KalmanMotion


class MultivariateKalmanFilter:

    def __init__(self, observation_dim: int, tracker_id, initial_position: None, sort=True, drop_after=5):
        # if not initial_position:
        #     initial_position = [0] * observation_dim

        # handle multiple KalmanFilter objects so
        # that we can achieve better performances
        self.tracker_id = tracker_id
        self.n_dims = observation_dim
        if sort:
            self.kfilters = KalmanBoxTracker(bbox_to_box_angles(initial_position))
        else:
            self.kfilters = [KalmanMotion(initial_state_mean=[initial_position[i], 0, 0]) for i in
                             range(observation_dim)]

        self.sort = sort

        # define state of multi-tracker
        self.lost_track = 0
        self.drop_after = drop_after

    def update(self, observation=None):
        if self.sort:
            # if obs is null this does nothing
            if observation:
                observation = bbox_to_box_angles(observation)
            self.kfilters.update(observation)
        else:
            raise NotImplementedError()

    def predict(self):
        """
        Predict new Kalman state at time t
        given all observations up to time t
        as well as the previous state t-1.
        Past observations are kept inside each
        Kalman Filter so that only the current
        one (time t) needs to be passed.
        :param observation: vector of shape observation_dim;
            each coordinate of this vector will be handled
            by its corresponding Kalman Filter.
        :return: prediction for next (combined) state.
        """

        # predict new state
        new_state = []
        if self.sort:
            # only return position
            return self.kfilters.predict()[0]
        else:
            raise NotImplementedError()

        # if not observation:
        #     observation = [ None ] * self.n_dims
        # for i, observation_coord in enumerate(observation):
        #     new_state.append(self.kfilters[i].predict(observation_coord))
        #
        # return new_state

    def get_state(self, tid: False):
        if self.sort:
            if tid:
                # add tracker id to last column
                box = box_angles_to_bbox(self.kfilters.get_state()[0])
                box = np.append(box, self.tracker_id)
                return box
            else:
                return self.kfilters.get_state()
        else:
            raise NotImplementedError()

    def increase_lost_track(self):
        self.lost_track += 1

    def is_dropped(self):
        return self.lost_track > self.drop_after

    def reset_fail_counter(self):
        self.lost_track = 0


def bbox_to_box_angles(box):
    (x, y, w, h) = box
    return x, y, x + w, y + h


def box_angles_to_bbox(box):
    """
    Convert box from (x1, y1, x2, y2) format
    to (x, y, w, h)
    """
    (x1, y1, x2, y2) = box
    return x1, y1, x2 - x1, y2 - y1


if __name__ == '__main__':
    k = MultivariateKalmanFilter(observation_dim=4, initial_position=[200, 150, 50, 92])
    obs = [200, 150, 50, 92]
    for i in range(20):
        obs[0] += 10 - (i * np.random.random())
        obs[1] += 4 + (i * np.random.random())
        if i % 5 == 0:
            print("NO observation")
            newstate = k.predict(None)
        else:
            print("Observation:", obs)
            newstate = k.predict(obs)
        print("New state:", [int(n) for n in newstate])
