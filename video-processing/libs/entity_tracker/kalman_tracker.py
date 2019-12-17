import numpy as np
from scipy.optimize import linear_sum_assignment
from libs.smoothing import MultivariateKalmanFilter


class KalmanTracker:
    """
    Multi-object tracker module focused
    on tracking object given detections;
    detections are assumed to be of shape
    (x, y, w, h).
    Tracker implementations used is the one
    provided through OpenCV interface; this
    class handles the logic and state of
    the multi-trackers.
    """

    def __init__(self, drop_after=10, max_trackers=100, ball_tracker=False):
        self.active_trackers = []
        self.dropped_trackers = []
        self.MAX_OBJECTS = max_trackers
        self.drop_after = drop_after
        self.tracker_counter = 0
        self.ball_tracker = ball_tracker

    def assign_prediction_to_detection(self, predictions, detections, eps, is_ball=False):
        """
        Match predictions to detections by
        looking at the predictions we generated
        at the previous time-step.
        Distance-based matching is performed with
        sensibility parameter eps.
        Matching detections to predictions is
        a minimum weight matching problem in a
        bi-partite graph.
        :param eps: max distance up to which we
        can consider 2 boxes to be matching.
        :param detections: bounding boxes coming
        from detector at current time-step.

        :return: 3 lists containing indices of detections and
        prev_predictions -matches (list of couples),
        unmatched_detections and unmatched_predictions.
        """
        # handle case in which either detections or predictions are missing
        if len(detections) == 0:
            return [], [], [i for i in range(len(predictions))]
        elif len(predictions) == 0:
            return [], [i for i in range(len(detections))], []

        # build matrices for simplifying computations (avoid last col)
        predm = np.array(predictions)
        detections = np.array(detections)

        # compute cost matrix
        sse = lambda x, y: min(np.sum((x - y) ** 2), eps)

        cost = np.zeros((len(detections), len(predm)))
        if not is_ball:
            for i, (x, y, w, h) in enumerate(detections):
                # dc = np.array( [x+w/2, y+h/2] )
                dc = np.array([x, y, x + w, y + h])
                for j, (x, y, w, h) in enumerate(predm):
                    # pc = np.array( [x + w / 2, y + h / 2] )
                    pc = np.array([x, w, x + w, y + h])
                    # cost[i, j] = cost_function(dc, pc)
                    cost[i, j] = -iou(dc, pc)
        else:
            # ball tracker will need a more 'forgiving'
            # metric since the speed is much higher wrt players
            for i, (x, y, w, h) in enumerate(detections):
                dc = np.array([x + w / 2, y + h / 2])
                for j, (x, y, w, h) in enumerate(predm):
                    pc = np.array([x + w / 2, y + h / 2])
                    cost[i, j] = sse(dc, pc)

        # solve minimum weight matching in bipartite graph problem
        # for assigning each detection to at most one prediction (cost matrix might be rectangular)
        # more here https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
        row_ind, col_ind = linear_sum_assignment(cost)
        # print("indices", row_ind, col_ind)
        print("Cost matrix", cost[row_ind, col_ind])
        matches = []
        # linear sum assignment will exclude nodes if cost is not a square matrix
        unmatched_d = [i for i in range(len(detections)) if i not in row_ind]
        unmatched_p = [i for i in range(len(predictions)) if i not in col_ind]
        # filter out assignments with higher cost than eps
        for i, cost_val in enumerate(cost[row_ind, col_ind]):
            if cost_val < eps:
                # matches will contain indices
                matches.append((row_ind[i], col_ind[i]))
            else:
                # this detection-prediction match is undone
                unmatched_d.append(row_ind[i])
                unmatched_p.append(col_ind[i])

        if is_ball:
            print("Matches(d,p):", matches)
            print("Unmatched prediction:", unmatched_p)
            print("Unmatched detection:", unmatched_d)

        return matches, unmatched_d, unmatched_p

    def track_players(self, bboxes, frame):
        """
        This method handles the policy
        through which each tracker's state
        gets updated.
        It must be called iteratively
        so that new predictions can be
        generated at each time step while
        detections are taken in input to
        adjust and update the trackers.
        This method matches detections to
        trackers predictions and tries to
        generate new positions from that.
        :param bboxes: set of detections sharing
        a common shape (x, y, w, h).
        :param frame: frame from video stream.
        :return: trackers predictions, a list of
        bounding boxes of same shape as bboxes,
        apart from an additional element 'tracker_id'
        in last position.
        """
        if len(bboxes) > self.MAX_OBJECTS:
            bboxes = bboxes[:self.MAX_OBJECTS]

        # get predictions at current time step
        # from active trackers
        predictions = [box_angles_to_bbox(tr.predict()) for tr in self.active_trackers]
        # todo assign player detections to predictions
        if not self.ball_tracker:
            matches, unmatched_d, unmatched_p = self.assign_prediction_to_detection(predictions, bboxes, eps=-0.01)
        else:
            matches, unmatched_d, unmatched_p = self.assign_prediction_to_detection(predictions, bboxes, eps=900,
                                                                                    is_ball=True)

        # create a 'new tracker' for each unmatched detection
        print(f'{len(unmatched_d)} unmatched detections were recognized (now creating new trackers)')
        for idx in unmatched_d:
            tid = self.tracker_counter
            self.tracker_counter += 1
            # use corresponding detection as initial state
            self.active_trackers. \
                append(MultivariateKalmanFilter(tracker_id=tid, observation_dim=4, initial_position=bboxes[idx],
                                                drop_after=self.drop_after))
            # new tracker and corresponding initial state is now a valid 'match'
            matches.append((idx, len(self.active_trackers) - 1))  # use indices instead of objs

        # update state of active trackers predictions
        for (det_id, tr_id) in matches:
            self.active_trackers[tr_id].update(bboxes[det_id])
            self.active_trackers[tr_id].reset_fail_counter()

        # increase the count of failures of corresponding tracker for each unmatched predictions
        print(f'{len(unmatched_p)} unmatched predictions were recognized (increasing failure counter)')
        for idx in unmatched_p:
            self.active_trackers[idx].increase_lost_track()
            # also update state of these trackers with no-observation
            self.active_trackers[idx].update(None)

        # predictions boxes (state of each tracker) # todo box angles to box width tranf inside
        predictions = [t.get_state(tid=True) for t in self.active_trackers]
        # print(predictions)
        # drop trackers (very efficiently ;) )
        self.active_trackers = [t for t in self.active_trackers if not t.is_dropped()]

        # return trackers predictions
        return predictions


def centroid_to_box(c, w, h):
    return [int(c[0] - w / 2), int(c[1] - h / 2), int(w), int(h)]


def box_to_centroid(box):
    if box is not None:
        return [int(box[0] + box[2] / 2), (box[1] + box[3] / 2)]
    else:
        return box


def box_angles_to_bbox(box):
    """
    Convert box from (x1, y1, x2, y2) format
    to (x, y, w, h)
    """
    (x1, y1, x2, y2) = box
    return x1, y1, x2 - x1, y2 - y1


def bbox_to_box_angles(box):
    (x, y, w, h) = box
    return x, y, x + w, y + h


def iou(bb_test, bb_gt):
    """
    Computes IUO between two bboxes in the form [x1,y1,x2,y2]
    """
    xx1 = np.maximum(bb_test[0], bb_gt[0])
    yy1 = np.maximum(bb_test[1], bb_gt[1])
    xx2 = np.minimum(bb_test[2], bb_gt[2])
    yy2 = np.minimum(bb_test[3], bb_gt[3])
    w = np.maximum(0., xx2 - xx1)
    h = np.maximum(0., yy2 - yy1)
    wh = w * h
    o = wh / ((bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1])
              + (bb_gt[2] - bb_gt[0]) * (bb_gt[3] - bb_gt[1]) - wh)
    return (o)
