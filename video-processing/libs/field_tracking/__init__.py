import json

import numpy as np
import cv2
from .utils import distance_matrix
from .fitting import FitFieldIndex, get_field_lines
from libs.smoothing import KalmanMotion


def find_optimal_assignments(transitions, final):
    n_states = transitions[0].shape[0]
    pred = np.empty((n_states, len(transitions)), dtype=np.int32)
    # cost = np.empty((n_states, len(transitions)), dtype=np.float32)
    cost = np.zeros(n_states)

    for i, T in enumerate(transitions):
        pred[:, i] = np.argmin(T + cost[:, None], axis=1)
        for j in range(n_states):
            cost[j] += T[j, pred[j, i]]

    cost += final
    w = np.argmin(cost)
    res = [w]
    for i in range(len(transitions)):
        v = pred[w, len(transitions) - 1 - i]
        res = [v] + res
        w = v

    return res


class CameraEstimator:
    def __init__(self, index_path="index.npz"):
        self.field_index = FitFieldIndex(index_path)

        self.frames = []

    def add_frame(self, lines_img):
        # filter lines
        _, components, stats, _ = cv2.connectedComponentsWithStats(lines_img)
        for i, (x, y, w, h, area) in enumerate(stats[1:]):
            # if it is (too square and too full) or area is too low remove detection
            if (0.6 <= w / h <= 1 / 0.6 and area >= 0.5 * w * h) or area <= 15:
                components[components == (i + 1)] = 0

        lines_img = np.where(components > 0, 255, 0).astype(np.uint8)
        cfgs, scores = self.field_index(lines_img)

        self.frames.append({
            # "lines": lines_img,
            "cfgs": cfgs,
            "scores": scores
        })

    def get_smooth_states(self, state_to_camera, target_sigma=1.0, eye_sigma=0.2, zoom_sigma=0.2, score_sigma=0.3):
        scale = np.asarray([target_sigma, target_sigma, eye_sigma, eye_sigma, eye_sigma, zoom_sigma])
        scale = 1 / (np.sqrt(2) * scale)

        transitions = []
        for i in range(0, len(self.frames) - 1):
            D = distance_matrix(self.frames[i]["cfgs"] * scale[None, :], self.frames[i + 1]["cfgs"] * scale[None, :],
                                squared=True)
            D += ((1 - self.frames[i]["scores"]) / score_sigma ** 2)[:, None]
            transitions.append(D)

        final = (1 - self.frames[-1]["scores"]) / score_sigma ** 2

        path = find_optimal_assignments(transitions, final)

        states = []
        old_state = None
        for w, f in zip(path, self.frames):
            if old_state is not None:
                d = np.hypot(old_state[0] - f["cfgs"][w][0], old_state[1] - f["cfgs"][w][1])
                if d < 6.0:
                    old_state = (f["cfgs"][w][0], f["cfgs"][w][1])
                    states.append(f["cfgs"][w])
                else:
                    states.append([np.NaN] * 6)
            else:
                old_state = (f["cfgs"][w][0], f["cfgs"][w][1])
                states.append(f["cfgs"][w])

        states = np.vstack(states)[:, (0, 1, 2, -1)]

        kalman = KalmanMotion(acc_var=1e-4, observation_var=8.0)
        states, _, _ = kalman.smooth(np.ma.masked_invalid(states))

        # # compute image to field transformation (tranformation matrices)
        # field_to_img = M @ camera.get_homography(frame.shape[1], frame.shape[0])
        # img_to_field = np.linalg.inv(M)
        #
        # lines = project_lines(field.lines, field_to_img)
        # # todo unite with player boxes to have debug version
        # draw_lines(frame, lines, (0, 255, 255), 3, requires_scaling=False)

        return [state_to_camera(state) for state in states]

    def save_states(self, name):
        frames = self.get_states()

        with open(name, "w") as f:
            json.dump(frames, f)

    def load_states(self, name):
        frames = json.load(open(name))

        self.set_states(frames)

    def get_states(self):
        return [{
            # "lines": lines_img,
            "cfgs": x["cfgs"].tolist(),
            "scores": x["scores"].tolist()
        } for x in self.frames]

    def set_states(self, frames):
        self.frames = [{
            # "lines": lines_img,
            "cfgs": np.asarray(x["cfgs"]),
            "scores": np.asarray(x["scores"])
        } for x in frames]
