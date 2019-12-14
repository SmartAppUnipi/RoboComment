import cv2
import numpy as np


def filter_predictions(predictions, min_conf=0.0, nms_threshold=1.0, classes=None, max_area=1e30, min_area=0.0, mask=None, mask_threshold=0.5):
    """
    Filter Yolo prediction and converts results to a more humane format
    :param predictions: raw yolo predictions
    :param min_conf:
    :param nms_threshold:
    :param classes: classes that will be considered
    :param max_area: max area of the bounding box
    :param min_area: min area of the bounding box
    :param mask: If specified selects only boxes that overlaps with the mask at least by mask_threshold
    :param mask_threshold:

    :return: boxes, confidences, class IDs
    """
    # if classes are not specified consider all classes
    if classes is None:
        classes = set(range(1000))

    boxes = []
    confidences = []
    cls_ids = []

    # parse predictions and filter by class and score
    for cx, cy, w, h, obj_score, cls_score, cls_id in predictions:
        # only consider given classes and filter by area
        if int(cls_id) in classes and min_area <= w * h <= max_area:
            # TODO consider other options
            confidence = obj_score * cls_score

            # filter out weak predictions
            if confidence >= min_conf:
                # convert box coordinates
                x = int(np.round(cx - (w / 2)))
                y = int(np.round(cy - (h / 2)))
                w = int(np.round(w))
                h = int(np.round(h))

                good = True
                if mask is not None:
                    good = (np.sum(mask[y:y+h, x:x+w]) / (w*h)) >= mask_threshold

                if good:
                    boxes.append((x, y, w, h))
                    confidences.append(float(confidence))
                    cls_ids.append(int(cls_id))

    # do Non Maximum Suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, min_conf, nms_threshold)
    if len(idxs):
        idxs = idxs.flatten()
        # actual filtering
        boxes = [boxes[i] for i in idxs]
        confidences = [confidences[i] for i in idxs]
        cls_ids = [cls_ids[i] for i in idxs]

        return boxes, confidences, cls_ids
    else:
        return [], [], []
