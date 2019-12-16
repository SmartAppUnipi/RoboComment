from flask import Flask, send_file, make_response
from flask_cors import CORS
import json
import cv2
from libs.field_tracking.field import SoccerField

app = Flask(__name__)
CORS(app)

cap = cv2.VideoCapture('videos/juve_attacking.mp4')
frames = []
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    frames.append(frame)
    if not ret:
        break

field = SoccerField()
# field_configs = json.load(open("camera.json"))
field_configs = json.load(open("data/videos/juve_attacking_smoothed_states.json"))
team_colors = ["white", "blue", "yellow"]


@app.route('/video_url', methods=["GET"])
def video_url():
    return "https://storage.googleapis.com/hlt_project/Off_Topic_SA/testvideo.mp4"


@app.route('/map/<int:i>', methods=["GET"])
def get_field_map(i):
    # field_to_img = np.asarray(field_configs[i]["field_to_img"])
    # people = field_configs[i]["people"]
    # balls = field_configs[i]["balls"]
    #
    # img_to_field = np.linalg.inv(field_to_img)
    # people = to_2d_homogeneous(people)
    # people = people @ img_to_field.T
    # people /= people[:, 2][:, None]

    # circles = [(x, y, "blue", 1.0) for x, y, _ in people]

    cfg = field_configs[i]

    circles = [(player["pos"][0], player["pos"][1], team_colors[player["team"]], 1.0, player["jersey"]) for player in
               cfg["players"]]
    circles.append((cfg["ball"]["pos"][0], cfg["ball"]["pos"][1], "white", 0.5, None))

    # if balls:
    #     balls = to_2d_homogeneous(balls)
    #     balls = balls @ img_to_field.T
    #     balls /= balls[:, 2][:, None]
    #
    #     circles += [(x, y, "white", 0.5) for x, y, _ in balls]

    response = make_response(field.svg(circles))
    response.headers.set('Content-Type', 'image/svg+xml')
    return response


@app.route('/frame/<int:i>', methods=["GET"])
def get_frame(i):
    # cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    # ok, frame = cap.read()
    # print(frame.shape)
    frame = frames[i]
    frame = cv2.resize(frame, (640, 360))
    retval, buffer = cv2.imencode('.jpeg', frame)

    response = make_response(buffer.tobytes())
    response.headers.set('Content-Type', 'image/jpeg')
    return response


@app.route("/")
def index():
    return send_file("static/index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
