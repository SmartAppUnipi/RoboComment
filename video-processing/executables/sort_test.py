from libs.entity_tracker.sort import Sort
import numpy as np
from libs.yolo.cache import YoloCache
import argparse
import cv2
from libs.yolo import filter_predictions


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", default="videos/juve_attacking.mp4",
                help="path to video")
ap.add_argument("-y", "--yolo-cache", default="",
                help="base path to YOLO cache for the video")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
                help="threshold when applying non-maxima suppression")
ap.add_argument("-tr", "--tracker", type=str, default="csrt",
                help="OpenCV object tracker type")
args = ap.parse_args()


# load yolo cache
yolo_cache_path = args.yolo_cache
if yolo_cache_path == "":
    yolo_cache_path = args.video[:-4] + "_cache.npz"
yolo = YoloCache(yolo_cache_path)

# load video 'stream'
cap = cv2.VideoCapture(args.video)
COLORS = [(100, 20, 20)] * 80
LABELS = []

#create instance of SORT
mot_tracker = Sort(max_age=200, min_hits=1)
frame_counter = 0
old_boxes = []
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    (H, W) = frame.shape[:2]

    # detect players in frame using Yolo net
    predictions = yolo.predict(frame)
    boxes, confidence, cls_ids = filter_predictions(predictions, classes=[0], min_conf=0.4, nms_threshold=0.2, max_area=4e4,
                                           min_area=4e2)

    input_ = []
    for (x, y, w, h), c in zip(boxes, confidence):
        input_.append((x, y, x+w, y+h, c))
    input_ = np.array(input_)

    # update SORT -
    # track_bbs_ids is a np array where each row contains a valid bounding box and track_id (last column)
    track_bbs_ids = mot_tracker.update(input_)
    # print(track_bbs_ids)
    # for d in detections:
    #     print(d)
    # for box in boxes:
    #     (x1, y1, w, h) = box
    #     color = [int(c) for c in (100, 20, 20)]
    #     cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), color, 2)


    #
    print('================')
    for t in track_bbs_ids:
        (x1, y1, x2, y2, tid) = t.astype(np.int32)
        print((x1, y1, x2, y2, tid))
        color = [int(c) for c in (100, 20, 20)]
        cv2.rectangle(frame, (x1, y1), (x2, y2), [100, 20, 20], 2)

        cv2.putText(frame, str(tid), (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Image", frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()