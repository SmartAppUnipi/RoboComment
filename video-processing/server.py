import json
import os
from flask import Flask, request, make_response
from flask_cors import CORS

from libs.utils.routes import RoutesParser
from libs.utils.json_builder import convert_to_symbolic_format
from threading import Thread

from main import main
from libs.utils import ServerArgs, get_team_numbers_from_kb

app = Flask(__name__)
CORS(app)

routes = RoutesParser()
_, port, path = routes["video"]
sym_host, sym_port, sym_path = routes["scene"]

print(f"Running on port {port} at {path}(POST)")


def stream_to_symbolic(frames: list, user_id: str, match_id, match_url):
    # gaysons = [convert_to_symbolic_format(frame, user_id) for frame in frames]
    # json.dump(gaysons, open("gayson.json", "w"))
    for frame in frames:
        gayson = convert_to_symbolic_format(frame, user_id, match_id, match_url)
        routes.post("scene", gayson)


def process_video(video_name, kb_response, user_id: str, match_id, match_url):
    # build args object
    # args = {'video': f'data/videos/{video_name}', 'recompute': True,
    #         'no_show': True, 'yolo_cache': "", 'confidence': 0.5, 'threshold': 0.3 } # not saving video
    args = {
        "video": f"data/videos/{video_name}",
        "confidence": 0.5,
        "threshold": 0.3,
        "limit": 0,
        'yolo_cache': "",
        "recompute": True,
        "run_yolo": False,
        "no_show": True,
        "tracker": "csrt",
        "save_video": "",
        "sort": False
    }
    args = ServerArgs(args)

    pnumbers = get_team_numbers_from_kb(kb_response)
    # process video
    main(args, pnumbers)
    # get result of processing phase
    smoothed_result = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/videos/",
                              video_name[:-4] + "_smoothed_states.json")
    frames = json.load(open(smoothed_result))

    stream_to_symbolic(frames, user_id, match_id, match_url)


def json_response(obj):
    response = make_response(json.dumps(obj))
    response.headers.set('Content-Type', 'application/json')
    return response


@app.route(path, methods=["POST"])
def post_video():
    req = request.get_json()
    user_id = req["user_id"]
    video_url = req["match_url"]
    match_id = req["match_id"]
    video_name = video_url[41:]
    print(f"User '{user_id}' requested video '{video_name}'")
 
    kb_response = routes.query_kb("qi", "match", match_id )
    print(kb_response)
    # get yolo cache path
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/videos/",
                              video_name[:-4] + "_cache.npz")

    # execute processing using pre-cached yolo results
    if os.path.exists(cache_path):
        print(f'Processing {video_name} video using {cache_path} yolo cache')
        thread = Thread(target=process_video, args=(video_name, kb_response, user_id, match_id, video_url))
        thread.start()
        # frames = json.load(open(cache_path))
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
