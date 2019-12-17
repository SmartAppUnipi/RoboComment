import cv2
import numpy as np


def pad_to_square(img):
    h, w = img.shape[:2]
    if h == w:
        return img

    size = max(h, w)
    h_pad = (size - w) // 2
    v_pad = (size - h) // 2

    return cv2.copyMakeBorder(img, v_pad, size - h - v_pad, h_pad, size - w - h_pad, cv2.BORDER_REPLICATE)


# greyscale image with some nerd weights found online
def rgb2gray(rgb):
    norm_image = cv2.normalize(rgb, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    # norm_image = rgb/255.

    return np.dot(norm_image, [0.2989, 0.5870, 0.1140])
