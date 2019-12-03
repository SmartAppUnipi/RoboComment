import numpy as np


def normalize_tracker_boxes(boxes, is_sort):
    """
    Convert tracker boxes to a standardized format (x, y, w, h)
    :param boxes: boxes obtained from tracker
    :param is_sort:
    :return: nomalized_boxes, tracks IDs
    """
    n_boxes = []
    track_ids = []
    for t in boxes:
        if is_sort:
            (x1, y1, x2, y2, tid) = t.astype(np.int32)
            x, y, w, h = min(x1, x2), min(y1, y2), np.abs(x2 - x1), np.abs(y2 - y1)
        else:
            (x, y, w, h, tid) = t
        if w > 10 and h > 10:
            n_boxes.append((int(max(x, 0)), int(max(y, 0)), int(w), int(h)))
            track_ids.append(int(tid))

    return n_boxes, track_ids
