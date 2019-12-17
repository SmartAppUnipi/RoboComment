import os
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from .utils import pad_to_square, rgb2gray
from .model import DenseModel


class JerseyRecogniser:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "models/jersey.weights")
        self.model = DenseModel()
        self.model.load_state_dict(torch.load(model_path, map_location="cpu"))

    def __call__(self, frame, player_boxes, possible_numbers):
        """
        :param frame:
        :param player_boxes: format (x, y, w, h)
        :return: [(recognized number, probability)]
        """
        # sanity check
        if len(player_boxes) == 0:
            return []

        # filter used to remove impossible numbers from results
        jersey_filter = np.ones(100, dtype=np.float32) * 1e20
        for x in possible_numbers:
            jersey_filter[x] = 0
        jersey_filter = torch.FloatTensor(jersey_filter)

        # crop player jerseys for number recognition
        jerseys = np.empty((len(player_boxes), 1, 48, 48), dtype=np.float32)

        for i, (x, y, w, h) in enumerate(player_boxes):
            y = int(y + 0.1 * h)
            h = int(0.4 * h)
            jerseys[i, 0] = rgb2gray(
                cv2.resize(pad_to_square(frame[y: y + h, x:x + w]), (48, 48), cv2.INTER_AREA).astype(
                    np.float32)) - 0.5

        with torch.no_grad():
            y = self.model(torch.FloatTensor(jerseys))
            y = F.softmax(y - jersey_filter, dim=-1).cpu().numpy()

        labels = np.argmax(y, axis=1)
        res = []
        for i in range(len(player_boxes)):
            res.append((str(labels[i]), float(y[i, labels[i]]), y[i].tolist()))

        return res
