import numpy as np
from pykalman import KalmanFilter


class KalmanMotion:
    def __init__(self, observation_var=1.0, pos_var=1e-4, speed_var=1e-3, acc_var=1e-2, initial_state_mean=[0, 0, 0],
                 initial_state_covariance=np.diag([1e5, 1e5, 1e5])):
        # specify parameters
        transition_matrix = [[1, 1, 0.5], [0, 1, 1], [0, 0, 1]]
        transition_offset = [0, 0, 0]
        observation_matrix = [[1, 0, 0]]
        observation_offset = [0]
        transition_covariance = np.diag([pos_var, speed_var, acc_var])
        observation_covariance = [[observation_var]]

        self.kf = KalmanFilter(
            transition_matrix, observation_matrix, transition_covariance,
            observation_covariance, transition_offset, observation_offset, initial_state_mean=initial_state_mean,
            initial_state_covariance=initial_state_covariance)

        # this will hold the observations collected at each time step
        self.obs_history = [
            initial_state_mean[0] + np.random.normal(scale=3)]  # todo leaving empty history fucks up dimensions

    def smooth(self, observations):
        """
        Smooth observations producing position, speed, acceleration
        :param observations: array of shape (# of observations, dimensions)
        :return: position, speed, acceleration: 3 arrays of shape (# of observations (up to time t), dimensions)
        """
        pos = []
        vel = []
        acc = []

        for i in range(observations.shape[1]):
            y, covariances = self.kf.smooth(observations[:, i])
            pos.append(y[:, 0].reshape(-1, 1))
            vel.append(y[:, 1].reshape(-1, 1))
            acc.append(y[:, 2].reshape(-1, 1))

        pos = np.hstack(pos)
        vel = np.hstack(vel)
        acc = np.hstack(acc)

        return pos, vel, acc

    def update_state(self):
        """
        Update state of Kalman Filter
        given all observation obtained
        so far (up to time t-1).
        :return:
        """
        # return initial state if no observation was yet
        if len(self.obs_history) == 0:
            return self.kf.initial_state_mean, self.kf.initial_state_covariance

        hist = np.ma.masked_array(self.obs_history, mask=np.zeros((1,)))
        for i in range(len(hist)):
            if hist[i] == -1e8:
                hist[i] = np.ma.masked

        # print(hist, hist.shape)
        return self.kf.filter(hist)

    def predict(self, observation):
        """
        Predict new Kalman state at time t
        given all observations up to time t
        as well as the previous state t-1.
        Past observations are kept inside this
        class so that only the current one
        needs to be passed.
        :param observation: vector of shape observation_dim.
        :return:
        """
        # input must contain past state, so we get it
        (state_mean, state_covariance) = self.update_state()

        # print("Update state:", state_mean, state_covariance)
        # predict new state
        # print("Previous state:", state_mean[0],"\nObservation:", observation)
        next_state_mean, next_state_covariance = self.kf.filter_update(state_mean[0], state_covariance[0], observation)
        # print("PREDICTION:", next_state_mean)

        # add observation to history
        if not observation:
            self.obs_history.append(-1e8)  # todo check out np.ma.compress_rows(np.ma.masked_invalid(trks))
        else:
            self.obs_history.append(observation)
        # print("Next state:", next_state_mean)

        # only return position out of the state coordinates pos, vel, acc
        return next_state_mean[0]
