import os
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from .svhn_model import Model
from .my_model import ModelEff


def _load_model():
    model_path = os.path.join(os.path.dirname(__file__), "models/model-54000.pth")

    if not os.path.exists(model_path):
        raise Exception(
            "Cannot find model, download it from 'https://drive.google.com/file/d/1DSg3F5GpouEvU9n7YSPdUKH1CSmkdwSw/view' and put in player_recognition/models/")

    model = Model()
    state = torch.load(model_path, map_location="cpu")
    for k in ["_hidden1.1.training", "_hidden1.4.training", "_hidden2.1.training", "_hidden2.4.training",
              "_hidden3.1.training", "_hidden3.4.training", "_hidden4.1.training", "_hidden4.4.training",
              "_hidden5.1.training", "_hidden5.4.training", "_hidden6.1.training", "_hidden6.4.training",
              "_hidden7.1.training", "_hidden7.4.training", "_hidden8.1.training", "_hidden8.4.training"]:
        del state[k]
    model.load_state_dict(state)
    return model


def pad_to_square(img):
    h, w = img.shape[:2]
    if h == w:
        return img

    size = max(h, w)
    h_pad = (size - w) // 2
    v_pad = (size - h) // 2

    return cv2.copyMakeBorder(img, v_pad, size - h - v_pad, h_pad, size - w - h_pad, cv2.BORDER_REPLICATE)


class JerseyRecogniser:
    def __init__(self):
        self.model = _load_model()

    def __call__(self, frame, player_boxes):
        """
        :param frame:
        :param player_boxes: format (x, y, w, h)
        :return: [(recognized number, probability)]
        """
        # crop player jerseys for number recognition
        jerseys = np.empty((len(player_boxes), 54, 54, 3), dtype=np.float32)

        for i, (x, y, w, h) in enumerate(player_boxes):
            y = int(y + 0.1 * h)
            h = int(0.4 * h)
            jerseys[i] = cv2.resize(pad_to_square(frame[y: y + h, x:x + w]), (54, 54), cv2.INTER_LINEAR).astype(
                np.float32) / 255 - 0.5

        # convert BGR -> RGB and to BATCH x CHANNEL x H x W
        jerseys = jerseys[:, :, :, (2, 1, 0)].transpose(0, 3, 1, 2)

        with torch.no_grad():
            length_logits, digit1_logits, digit2_logits, _, _, _ = self.model(torch.FloatTensor(jerseys))
            length_logits = F.softmax(length_logits, dim=-1).cpu().numpy()
            digit1_logits = F.softmax(digit1_logits, dim=-1).cpu().numpy()
            digit2_logits = F.softmax(digit2_logits, dim=-1).cpu().numpy()

        lengths = np.argmax(length_logits, axis=1)
        digit1 = np.argmax(digit1_logits, axis=1)
        digit2 = np.argmax(digit2_logits, axis=1)

        res = []
        for i in range(len(player_boxes)):
            # compute probability of recognition
            p = length_logits[i, lengths[i]] * digit1_logits[i, digit1[i]]

            length = max(1, min(2, lengths[i]))
            if length == 2:
                p *= digit2_logits[i, digit2[i]]
                res.append((str(digit1[i]) + str(digit2[i]), p))
            else:
                res.append((str(digit1[i]), p))

        return res


class JerseyRecogniserEff:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "models/model_eff.weights")
        self.model = ModelEff()
        self.model.load_state_dict(torch.load(model_path, map_location="cpu"))

    def __call__(self, frame, player_boxes):
        """
        :param frame:
        :param player_boxes: format (x, y, w, h)
        :return: [(recognized number, probability)]
        """
        # crop player jerseys for number recognition
        jerseys = np.empty((len(player_boxes), 48, 48, 3), dtype=np.float32)

        for i, (x, y, w, h) in enumerate(player_boxes):
            y = int(y + 0.1 * h)
            h = int(0.4 * h)
            jerseys[i] = cv2.resize(pad_to_square(frame[y: y + h, x:x + w]), (48, 48), cv2.INTER_AREA).astype(
                np.float32) / 255 - 0.5

        # convert to BATCH x CHANNEL x H x W
        jerseys = jerseys.transpose(0, 3, 1, 2)

        with torch.no_grad():
            y = self.model(torch.FloatTensor(jerseys))
            y = F.softmax(y, dim=-1).cpu().numpy()

        labels = np.argmax(y, axis=1)
        res = []
        for i in range(len(player_boxes)):
            res.append((str(labels[i]), float(y[i, labels[i]])))

        return res
