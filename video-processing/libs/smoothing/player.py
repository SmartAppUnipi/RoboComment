import numpy as np
from collections import Counter
from .motion import KalmanMotion


def smooth_player_track(track):
    kalman = KalmanMotion()
    positions = np.asarray([x["pos"] for x in track])
    pos, speed, _ = kalman.smooth(positions)

    # choose most common jersey number (TODO better scoring)
    jersey_scores = np.zeros(100)
    team_scores = Counter()
    for x in track:
        jersey_scores += np.log(0.7 + np.asarray(x["jersey"][2]))
        team_scores[x["team"]] += 1

    jersey = int(np.argmax(jersey_scores))  # jersey_scores.most_common(1)[0][0]
    team = team_scores.most_common(1)[0][0]

    for x, p, s in zip(track, pos, speed):
        x["pos"] = p.tolist()
        x["speed"] = s.tolist()
        x["jersey"] = jersey
        x["team"] = team


def smooth_ball(states):
    # compute track lengths
    track_length = Counter()
    for state in states:
        for ball in state["ball"]:
            track_length[ball["track"]] += 1

    # at every frame choose the longest track
    ball_pos = []
    for state in states:
        winner = (np.NaN, np.NaN)
        winner_score = 5
        for ball in state["ball"]:
            distance_from_field_circle = np.hypot(ball["pos"][0] - 11.0, ball["pos"][1] - 34)
            distance_from_field_circle = min(np.hypot(ball["pos"][0] - 105.0 + 11.0, ball["pos"][1] - 34),
                                             distance_from_field_circle)
            if track_length[ball["track"]] > winner_score and distance_from_field_circle > 3.0:
                winner_score = track_length[ball["track"]]
                winner = ball["pos"]

        ball_pos.append(winner)

    positions = np.ma.masked_invalid(np.asarray(ball_pos))
    kalman = KalmanMotion(observation_var=1.0)
    pos, speed, _ = kalman.smooth(positions)

    return [{
        "pos": (p[0], p[1]),
        "speed": (s[0], s[1]),
    } for p, s in zip(pos, speed)]


def smooth_players_and_balls(states):
    tracks = dict()
    for i, state in enumerate(states):
        for player in state["players"]:
            track_id = player["track_id"]
            if track_id not in tracks:
                tracks[track_id] = []

            tracks[track_id].append({
                "frame": i,
                "box": player["box"],
                "track_id": player["track_id"],
                "pos": player["pos"],
                "jersey": player["jersey"],
                "team": player["team"]
            })

    smoothed_states = [{"players": list(), "ball": ball} for ball in smooth_ball(states)]

    for trk_id in tracks:
        smooth_player_track(tracks[trk_id])
        for x in tracks[trk_id]:
            frame = x["frame"]
            smoothed_states[frame]["players"].append({
                "box": x["box"],
                "track_id": x["track_id"],
                "pos": x["pos"],
                "speed": x["speed"],
                "jersey": x["jersey"],
                "team": x["team"],
                "track": trk_id
            })

    return smoothed_states
