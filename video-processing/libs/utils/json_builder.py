def coord(x=0, y=0, confidence=1):
    return {'x': x, 'y': y, 'confidence': confidence}


def coord3d(x=0, y=0, z=0):
    return {'x': x, 'y': y, 'z': z}


def uncertain_value(value, confidence=1):
    return {'value': value, 'confidence': confidence}


def get_camera(position, target, zoom):
    return {"position": coord3d(*position), "target": coord(*target), "zoom": zoom}


def get_player(position, speed, pid, team, pose=""):
    if team == 2:
        team = -1

    return {
        "position": coord(*position),
        "speed": coord(*speed),
        "id": uncertain_value(int(pid)),
        "team": uncertain_value(team),
        "pose": pose
    }


def get_ball(position, speed, midair="false", owner=-1, owner_team=-1):
    return {
        'position': coord(*position),
        'speed': coord(*speed),
        'midair': uncertain_value(midair, 0),
        'owner': uncertain_value(owner, 0),
        'owner team': uncertain_value(owner_team, 0)
    }


def convert_to_symbolic_format(frame, user_id, match_id, match_url):
    camera = frame["camera"]

    res = {
        "user_id": user_id,
        "match_id": match_id,
        "match_url": match_url,
        "time": frame["relative time"],
        "camera": get_camera(camera["position"], camera["look_at"][:2], camera["zoom"]),
        "players": [get_player(p["pos"], p["speed"], p["jersey"], p["team"]) for p in frame["players"]],
        "ball": [get_ball(frame["ball"]["pos"], frame["ball"]["speed"])]
    }

    return res
