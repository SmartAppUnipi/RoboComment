# Football Video Processing

## Yolo module
Yolo module contains two main functionalities the yolo network itself and a cache that can be used to speedup work.
### Yolo Network
Yolo network is implemented in pytorch (to efficiently use the GPU) using a sliding window to take advantage of the full image resolution. Yolo config and weights can be downloaed by running the script `yolo/models/download.sh`.
The model can be used as follows:
```python
from libs.yolo import get_device, Yolo

# read the model and move it to the GPU (if available)
device = get_device()
yolo = Yolo("yolo/models/yolov3-spp.cfg", device)

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
Once compiled openpose, posedetector.py needs to be placed in "openpose\build\examples\tutorial_api_python"
Usage:
```python
from posedetector import get_pose_event
events = get_pose_event(impath)
```
return a list of tuples < filename, is_offside, is_something >
