import cv2
import os
from tqdm import tqdm
from libs.yolo import get_device, Yolo
from libs.yolo.cache import YoloCache

device = get_device()
yolo = Yolo("yolo/models/yolov3-spp.cfg", device)

for filename in ["juve_attacking", "gonzalo_goal", "dybala_goal", "counterattack"]:
    cache_path = f"videos/{filename}_cache.npz"
    if not os.path.exists(cache_path):
        cap = cv2.VideoCapture(f"videos/{filename}.mp4")
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