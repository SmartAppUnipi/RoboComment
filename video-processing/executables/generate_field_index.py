import numpy as np
import cv2
from tqdm import tqdm
from libs.field_tracking.camera import Camera, draw_lines
from libs.field_tracking.field import SoccerField

# get field polygon
field = SoccerField()

k = 1
zoom_k = 5
scale = 1

cfgs = []
for dx in range(5*k, 100*k):
    for dy in range(5*k, 65*k):
        for f in range(3*zoom_k, 8*zoom_k):
            # camera x position has been regressed by manual fitting
            dex = 0.08494764*dx/k + 48.03757
            cfgs.append((dx/k, dy/k, dex, 0, 0, f/zoom_k))

print(len(cfgs))

# cfgs = np.empty((50000, 3), dtype=np.float32)
imgs = np.empty((len(cfgs), scale**2 * 9 * 16), dtype=np.uint8)

for i, (dx, dy, dex, dey, dez, f) in enumerate(tqdm(cfgs)):
    # dx = np.random.uniform(-40.0, 40)
    # dy = np.random.uniform(-30.0, 30.0)
    # f = np.random.uniform(3.0, 3.4)

    camera = Camera([dex, -32.5 + dey, 14.0 + dez], [dx, dy, 0], f)

    lines = camera.project_lines(field.lines)
    img = draw_lines((8 * 9, 8 * 16), lines, 255)

    tmp = img.copy()
    img = img.astype(np.float32) / 255
    for _ in range(3):
        tmp = cv2.dilate(tmp, np.ones((3, 3), dtype=np.uint8))
        img += tmp.astype(np.float32) / 255

    img /= np.max(img)
    img = (img * 255).astype(np.uint8)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    img = cv2.resize(img, (scale * 16, scale * 9), interpolation=cv2.INTER_AREA)

    imgs[i] = img.reshape(-1)

np.savez("index5_small.npz", cfgs=np.asarray(cfgs, dtype=np.float32), imgs=imgs)
