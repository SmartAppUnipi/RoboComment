import json
import os
from flask import Flask, request, make_response
from flask_cors import CORS

from libs.utils.routes import RoutesParser
from libs.utils.json_builder import convert_to_symbolic_format
from threading import Thread

app = Flask(__name__)
CORS(app)

routes = RoutesParser()
_, port, path = routes["video"]
sym_host, sym_port, sym_path = routes["scene"]

print(f"Running on port {port} at {path}(POST)")


def stream_to_symbolic(frames: list, user_id: str):
    for frame in frames:
        gayson = convert_to_symbolic_format(frame, user_id)
        routes.post("scene", gayson)


def json_response(obj):
    response = make_response(json.dumps(obj))
    response.headers.set('Content-Type', 'application/json')
    return response


@app.route(path, methods=["POST"])
def post_video():
    req = request.get_json()
    user_id = req["user_id"]
    video_url = req["match_url"]
    video_name = video_url[41:]
    print(f"User '{user_id}' requested video '{video_name}'")

    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/videos/",
                              video_name[:-4] + "_smoothed_states.json")
    if os.path.exists(cache_path):
        frames = json.load(open(cache_path))
        thread = Thread(target=stream_to_symbolic, args=(frames, user_id))
        thread.start()
        return json_response({"ok": True, "msg": ""})
    else:
        print(f"There is no cache for the requested video ({cache_path})")
        return json_response({"ok": False, "msg": "Sorry we cannot give you commentary for that video yet"})

    # with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mocks/dummy.json"), "r") as f:
    #     data = json.load(f)
    #
    # for x in data:
    #     code = routes.post("scene", x)
    #     print(f"Symbolic response code {code}")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
