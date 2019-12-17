import numpy as np
import torch

from .models import Darknet


def get_device():
    if torch.cuda.is_available():
        print(f"Found GPU {torch.cuda.get_device_name(0)}")
        return torch.device("cuda")
    else:
        return torch.device("cpu")


class Yolo:
    def __init__(self, cfg_path, device=None, half=False):
        if device:
            self.device = device
        else:
            self.device = get_device()

        self.half = half

        self.model = Darknet(cfg_path)
        self.model.load_darknet_weights(cfg_path[:-4] + ".weights")
        if half:
            self.model = self.model.half()
        self.model = self.model.to(device)
        # bug on my pc (doesn't work without cuda call)
        # self.model = self.model.cuda()

        self.model.eval()

    def predict(self, img, min_conf=0.2, overlap=0.2, yolo_size=320):
        """
        Run Yolo using a sliding window to cover the entire image without reducing resolution
        :param img: image
        :param min_conf: boxes with object confidence < min_conf will be discarded
        :param overlap: amount of overlap between neighboring windows
        :param yolo_size: size of the window given to yolo as input. Big = faster, small = more accurate (I think)
        :return: 2D numpy array where each row contains: x, y, w, h, object_score, class_score, class_id
        """
        windows = []
        win_positions = []

        # computes step size to have overlapping windows
        s = int(yolo_size * (1 - overlap))

        # crop image at each window
        v_steps = int(np.floor(img.shape[0] / s)) + 1
        h_steps = int(np.floor(img.shape[1] / s)) + 1
        for i in range(h_steps):
            x = min(s * i, img.shape[1] - yolo_size)
            for j in range(v_steps):
                y = min(s * j, img.shape[0] - yolo_size)

                # keep track of positions
                win_positions.append((x, y))
                windows.append(self._prepare_image(img[y:y + yolo_size, x:x + yolo_size]))

        # pack batch and feed to yolo
        with torch.no_grad():
            batch = torch.FloatTensor(np.vstack(windows))
            if self.half:
                batch = batch.half()
            batch = batch.to(self.device)
            y = self.model(batch).cpu().numpy()

        all_predictions = []
        # for each image in batch (window on the image)
        for win_pos, win_predictions in zip(win_positions, y):
            # discard predictions with confidence < min_conf
            win_predictions = win_predictions[win_predictions[:, 4] >= min_conf]

            # compute class_id and corresponding class confidence
            class_id = np.argmax(win_predictions[:, 5:], axis=1).reshape(-1, 1)
            class_conf = np.max(win_predictions[:, 5:], axis=1).reshape(-1, 1)

            win_predictions = np.hstack((win_predictions[:, :5], class_conf, class_id))

            # add window position to align boxes to the image
            win_predictions += (*win_pos, 0, 0, 0, 0, 0)

            all_predictions.append(win_predictions)

        return np.vstack(all_predictions)

    @staticmethod
    def _prepare_image(img):
        """
        Convert a BGR image with shape (w,h,c) to a float RGB image in range [0, 1] with shape (c, w, h).
        Basically OpenCV image ===> torch image
        :param img: Color image in BGR format (OpenCV default)
        """
        return img[np.newaxis, :, :, ::-1].astype(np.float32).transpose((0, 3, 1, 2)) / 255.0
