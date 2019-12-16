import cv2
import numpy as np
import torch
import torch.nn as nn


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        c = 16

        self.convs = nn.Sequential(
            nn.Conv2d(1, c, 9, stride=2, padding=4),
            nn.ReLU(),
            nn.Conv2d(c, c, 5),
            nn.ReLU(),
            nn.Conv2d(c, 32, 3),
            nn.ReLU(),
        )

        self.linear = nn.Sequential(
            nn.Linear(4608, 64),
            nn.ReLU(),
            nn.Linear(64, 6)
        )

    def forward(self, x):
        # apply convolutions
        y = self.convs(x)

        return self.linear(y.view(y.size(0), -1))


class NeuralFieldIndex:
    def __init__(self, path):
        self.model = Model()
        self.model.load_state_dict(torch.load(path, map_location="cpu"))

    def __call__(self, img):
        img = cv2.resize(img, (int(8 * 16), int(8 * 9)), interpolation=cv2.INTER_LINEAR)
        tmp = img.copy()
        img = img.astype(np.float32) / 255
        for _ in range(3):
            tmp = cv2.dilate(tmp, np.ones((3, 3), dtype=np.uint8))
            img += tmp.astype(np.float32) / 255

        size = 3
        f = cv2.resize(img, (int(size * 16), int(size * 9)), interpolation=cv2.INTER_AREA)
        f /= np.max(f)
        f = f.astype(np.float32) * 255
        cv2.imwrite("f.png", f)
        #

        x = torch.FloatTensor(f/255).unsqueeze(0).unsqueeze(0)
        with torch.no_grad():
            return self.model(x).cpu().numpy()
