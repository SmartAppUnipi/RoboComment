import cv2
import os
from tqdm import tqdm
from libs.yolo.yolo import get_device, Yolo
from libs.yolo.cache import YoloCache
import torch

device = get_device()
# device = torch.device("cpu")
yolo = Yolo("libs/yolo/models/yolov3.cfg", device, half=False)

for filename in ["barca_goal_2", "tiki-taka", "inter-counterattack"]:
    cache_path = f"data/videos/{filename}_cache.npz"
    if not os.path.exists(cache_path):
        cap = cv2.VideoCapture(f"data/videos/{filename}.mp4")
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        cache = YoloCache(cache_path)
        cache.clear()

        for i in tqdm(range(total_frames)):
            ok, img = cap.read()
            if not ok:
                break

            predictions = yolo.predict(img)
            cache.add(predictions)

        cache.save()
