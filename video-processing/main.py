import json
import os

import cv2
import numpy as np
import argparse
import time
from libs.team_recognition import TeamRecognizer

# tracker
from libs.entity_tracker.kalman_tracker import KalmanTracker
from libs.entity_tracker.sort import Sort
from libs.entity_tracker.utils import normalize_tracker_boxes

# yolo
from libs.yolo.cache import YoloCache
from libs.yolo.filtering import filter_predictions

# field detection
from libs.field_tracking import CameraEstimator, get_field_lines
from libs.field_tracking.camera import Camera, draw_lines, project_lines
from libs.field_tracking.field import SoccerField

# player recognition
from libs.player_recognition import JerseyRecogniserEff

from libs.smoothing.player import smooth_players_and_balls


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", default="data/videos/juve_attacking.mp4",
                    help="path to video")
    ap.add_argument("-y", "--yolo-cache", default="",
                    help="base path to YOLO cache for the video")
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold", type=float, default=0.3,
                    help="threshold when applying non-maxima suppression")
    ap.add_argument("--limit", type=int, default=0,
                    help="Limit only the execution to the first n frames")
    ap.add_argument("--recompute", action="store_true", help="If specified recompute states")

    ap.add_argument("-tr", "--tracker", type=str, default="csrt",
                    help="OpenCV object tracker type")
    ap.add_argument("-sv", "--save-video", type=str, default='',
                    help="Save output of system to video file")
    ap.add_argument("-sort", "--sort", type=str, default=False,
                    help="Use SORT tracker")
    return ap.parse_args()


def get_yolo_cache(args):
    yolo_cache_path = args.yolo_cache
    if yolo_cache_path == "":
        yolo_cache_path = args.video[:-4] + "_cache.npz"
    return YoloCache(yolo_cache_path)


def yolo_predict(yolo, frame, field_mask):
    predictions = yolo.predict(frame)
    player_boxes, pconf, _ = filter_predictions(predictions, classes=[0], min_conf=0.3, nms_threshold=0.2,
                                                max_area=4e4,
                                                min_area=5e2, mask=field_mask)
    ball_boxes, bconf, _ = filter_predictions(predictions, classes=[32], min_conf=0.4, nms_threshold=0.2,
                                              max_area=1e4,
                                              mask=field_mask)

    return player_boxes, pconf, ball_boxes, bconf


def project_to_field(box, img_to_field):
    img_x = box[0] + box[2] / 2
    img_y = box[1] + box[3]

    # project onto field
    pos = np.asarray([img_x, img_y, 1])
    pos = pos @ img_to_field.T
    pos /= pos[2]

    return pos[0], pos[1]


def main():
    args = parse_arguments()

    # load yolo cache
    yolo = get_yolo_cache(args)

    # load video 'stream'
    cap = cv2.VideoCapture(args.video)
    fps = cap.get(cv2.CAP_PROP_FPS)

    states_path = args.video[:-4] + "_states.json"
    output_path = args.video[:-4] + "_smoothed_states.json"
    need_to_compute_states = (not os.path.exists(states_path)) or args.recompute

    # if needed prepare video output
    out = None
    if args.save_video:
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        out = cv2.VideoWriter(args.save_video, fourcc, fps, (1280, 720))

    #
    team_rec = TeamRecognizer(eps=.03)

    if args.sort:
        tracker = Sort(max_age=200, min_hits=1)
    else:
        tracker = KalmanTracker(max_trackers=300, drop_after=1)

    # todo IOU might be really not the best choice for the ball
    ball_tracker = KalmanTracker(max_trackers=50, drop_after=4)

    # load index containing different camera angles to fit
    camera_estimator = CameraEstimator("data/field_lines_index.npz")

    jersey_recognizer = JerseyRecogniserEff()

    frame_size = ()
    frames = []
    states = []
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        frames.append(frame)
        if not ret:
            break
        frame_size = (frame.shape[1], frame.shape[0])

        if need_to_compute_states:
            s = time.time()
            # detect field and field lines
            field_mask, field_lines = get_field_lines(frame)
            # detect players and balls in frame using Yolo net
            player_boxes, pconf, ball_boxes, bconf = yolo_predict(yolo, frame, field_mask)
            print("Time (lines + yolo):", time.time() - s)

            ############################
            # PLAYER AND BALL TRACKING #
            ############################
            tr_boxes = tracker.track_players(player_boxes, frame)
            bl_boxes = ball_tracker.track_players(ball_boxes, frame)

            tr_boxes, track_ids = normalize_tracker_boxes(tr_boxes, args.sort)

            ####################
            # TEAM RECOGNITION #
            ####################
            teams, _ = team_rec.detect_teams(frame, tr_boxes, use_idf=True)

            ######################
            # PLAYER RECOGNITION #
            ######################
            s = time.time()
            player_numbers = jersey_recognizer(frame, tr_boxes)
            print("Player recognition time", time.time() - s)
            print("Recognized players [(number, confidence)]", player_numbers)

            for (x, y, w, h), track_id, (jersey_number, _), team in zip(tr_boxes, track_ids, player_numbers, teams):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, f"({track_id}, {jersey_number}, {team})", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (250, 0, 10), 2)

            for i, (x, y, w, h, tid) in enumerate(bl_boxes):
                (x, y, w, h) = (int(x), int(y), int(w), int(h))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.putText(frame, str(tid), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 100, 10), 2)

            ###################
            # FIELD DETECTION #
            ###################
            # remove players and ball from line detection
            for x, y, w, h in ball_boxes + player_boxes:
                field_lines[y - 15:y + h + 30, x - 10:x + w + 20] = 0

            # add frame to camera estimator for future smoothing
            camera_estimator.add_frame(field_lines)

            ############################
            # SAVE CURRENT FRAME STATE #
            ############################

            current_state = {
                "ball": [x.tolist() for x in bl_boxes],
                "players": []
            }

            for box, track_id, jersey, team in zip(tr_boxes, track_ids, player_numbers, teams):
                current_state["players"].append({
                    "box": box,
                    "track_id": track_id,
                    "jersey": jersey,
                    "team": int(team)
                })

            states.append(current_state)

            # draw a bounding box rectangle and label on the image
            # todo write code to draw properly
            # Display the resulting frame
            # c = 0
            # loop over the indexes we are keeping
            # for i, ok in enumerate(unrecognized_boxes):
            #     if ok:
            #         # extract the bounding box coordinates
            #         (x, y) = (player_boxes[i][0], player_boxes[i][1])
            #         (w, h) = (player_boxes[i][2], player_boxes[i][3])
            #
            #         # draw a bounding box rectangle and label on the image
            #         color = [0, 0, 255]
            #         cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            #         # text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            #
            #         name = ['A', 'B', 'C']
            #         cv2.putText(frame, name[teams[c]], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 0, 0], 2)
            #         c += 1

        # optionally save video
        if args.save_video:
            out.write(frame)

        if 0 < args.limit <= len(frames):
            break

        if need_to_compute_states:
            # show the output image
            cv2.imshow("Image", frame)
            if cv2.waitKey(40) & 0xFF == ord('q'):
                break

    if need_to_compute_states:
        camera_states = camera_estimator.get_states()

        with open(states_path, "w") as f:
            json.dump({
                "camera": camera_states,
                "states": states
            }, f)

    ###############################
    # DO SMOOTHING AND PROJECTION #
    ###############################
    camera_states, states = [json.load(open(states_path))[k] for k in ["camera", "states"]]
    camera_estimator.set_states(camera_states)

    # San Siro config
    cameras = camera_estimator.get_smooth_states(lambda x: Camera([x[2], -32.5, 14.0], [x[0], x[1], 0], x[3]))

    # project players onto field
    for camera, state in zip(cameras, states):
        field_to_img = camera.get_homography(*frame_size)
        img_to_field = np.linalg.inv(field_to_img)

        for player in state["players"]:
            player["pos"] = project_to_field(player["box"], img_to_field)

        state["ball"] = [{
            "pos": project_to_field(ball, img_to_field),
            "track": ball[-1]
        } for ball in state["ball"]]

    smoothed_states = smooth_players_and_balls(states)
    # add relative time to states
    for i, (camera, state) in enumerate(zip(cameras, smoothed_states)):
        state["relative time"] = i / fps
        state["camera"] = {
            "position": camera.camera_position.tolist(),
            "zoom": float(camera.zoom_level),
            "look_at": camera.look_at.tolist(),
        }

    # save output
    with open(output_path, "w") as f:
        json.dump(smoothed_states, f)

    field = SoccerField()

    for camera, frame in zip(cameras, frames):
        field_to_img = camera.get_homography(frame.shape[1], frame.shape[0])
        img_to_field = np.linalg.inv(field_to_img)
        lines = project_lines(field.lines, field_to_img)

        draw_lines(frame, lines, (0, 255, 255), 3, requires_scaling=False)

        # show the output image
        cv2.imshow("Image", frame)
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


main()
