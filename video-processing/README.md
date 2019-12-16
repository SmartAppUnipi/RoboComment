# Football Video Processing

## Members:
- Lucchesi Nicolò
- Medioli Matteo
- Ronchetti Matteo
- Straface Michele

## EXTERNAL INTERFACES
\
\
**UI MODULE: Incoming flows**

**Endpoint** : "video"

**Method** : `POST`

**REQUEST RESULT**

```json
{
    "match_id": 10,
    "match_url": "https://someurl/video.mp4",
    "user_id": 1
}
```
\
\
**KNOWLEDGE BASE: Outcoming flows**

**Endpoint** : "qi"

**Method** : `POST`

**REQUEST RESULT**

```json
{
    "home": {
        "id": 3161,
        "name": "FC Internazionale Milano"
    },
    "away": {
        "id": 3159,
        "name": "Juventus FC"
    },
    "result": [
        "1",
        "2"
    ],
    "home_team": [
        {
            "id": "21094",
            "name": "D. D'Ambrosio",
            "club": 3161,
            "role": "Defender",
            "number": "33"
        },
       ...
    ],
    "away_team": [
       {
            "id": "1111111",
            "name": "De Ligt",
            "club": 3159,
            "role": "Defender",
            "number": "4"
        },
        ...
    ]
}
```
\
\
**SYMBOLIC LEVEL: Outcoming flows**

**Endpoint** : "scene"

**Method** : `POST`

**OUTPUT**

```json
{
    "time": "float, seconds",
    "camera": {
        "position": "instance of Coordinate3D, is the position of the camera in the field",
        "target": "instance of Coordinate, is the position of the target of the camera on the field",
        "zoom": "float range TBD"
    },
    "players": [
        {
            "position": "instance of Coordinate",
            "speed": "instance of Coordinate",
            "id": "instance of UncertainValue with value = int that identifies the person",
            "team": "instance of UncertainValue with value = int 0, 1 or -1 if the team is the referee",
            "pose": "optional string"
        }
    ],
    "ball": [
        {
            "position": "instance of Coordinate",
            "speed": "instance of Coordinate",
            "midair": "float between 0 and 1 (0 = ground, 1 = surely flying)",
            "owner": "instance of UncertainValue where value is the index of the player in the 'players' field",
            "owner team": "instance of UncertainValue where value is 0 or 1"
        }
    ]
}
```

## Usage
Run `./setup` to download YOLO weights (optional parameter `yolo320` makes it so you can download the lighter version).

Run `data/videos/download.sh` from bash shell to get some `.mp4` clips for testing.

Also make sure to have the index file downloaded in `data` directory through this [link](https://drive.google.com/file/d/1ZvZU8r5MxxMb42wniA1eb2v4txtjmNoo/view?usp=sharing).


## Yolo module
Yolo module contains two main functionalities the yolo network itself and a cache that can be used to speedup development phase on laptops.
### Yolo Network
Yolo network is implemented in pytorch (to efficiently use the GPU) using a sliding window to take advantage of the full image resolution. Yolo config and weights can be downloaed by running the script `yolo/models/download.sh`.
The model can be used as follows:
```python
from libs.yolo.yolo import get_device, Yolo

# read the model and move it to the GPU (if available)
device = get_device()
yolo = Yolo("yolo/models/yolov3.cfg", device)

# get a frame with opencv
# img = ...

predictions = yolo.predict(img)
```
`predictions` is a 2D numpy array where each row contains: x, y, w, h, object_score, class_score, class_id.

ATTENTION! NMS should be applied to predictions.

### Yolo Cache
Sample usage:
```python
cap = cv2.VideoCapture('videos/juve_attacking.mp4')
cache = YoloCache('videos/juve_attacking_cache.npz')

for i in range(10):
    _, img = cap.read()
    predictions = cache.predict(img)
```
`predictions` are same as above.

ATTENTION! `cache.predict` doesn't take into consideration the input, it just returns the next cached prediction.

## Sample Videos
Yolo caches for a few sample videos are included in the repository. To download the corresponding videos run `videos/download.sh`

## Pose

Usage:
```python
from libs.pose import PoseDetector
pose = posedetector.getpose(box=referee_box)
```
returns referee pose as string
