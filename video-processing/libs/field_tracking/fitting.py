import time

import numpy as np
import cv2
from scipy.spatial import cKDTree
from .utils import distance_matrix, norm
from .camera import sensor_to_image_projection
import matplotlib.pyplot as plt


def get_field_mask(img, field_color):
    tmp = img.reshape(-1, 3)
    g = distance_matrix(tmp, field_color.reshape(1, 3), squared=True)

    g = g.reshape(img.shape[0], img.shape[1])

    g = (g < 0.02).astype(np.uint8)

    #
    kernel = np.ones((9, 9), np.uint8)
    g = cv2.morphologyEx(g, cv2.MORPH_OPEN, kernel)
    g = cv2.morphologyEx(g, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
    g = cv2.morphologyEx(g, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))
    # plt.imshow(g)
    # plt.show()

    return g


def get_field_lines(img):
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    tmp = frame.astype(np.float32) / 255

    # get mean color, it should be close to field color (TODO something better)
    field_color = np.mean(tmp[-300:-100].reshape(-1, 3), axis=0)

    # create a rough mask of the field area
    field_mask = get_field_mask(tmp, field_color)

    # compute weights that convert image to grayscale that make the field as dark as possible and preserve whites
    A = np.asarray([field_color, [0.25, 0.23, 0.83]])
    b = np.asarray([0, 1])
    w = np.linalg.lstsq(A, b, rcond=None)[0].astype(np.float32)

    # convert to grayscale
    tmp = tmp.reshape(-1, 3).dot(w).reshape(frame.shape[0], frame.shape[1])

    # find high contrast areas
    f = np.asarray([[-0.5, -1, 0, 1, 0.5]], dtype=np.float32)
    vertical = np.abs(cv2.filter2D(tmp, cv2.CV_32F, f.T))
    horizontal = np.abs(cv2.filter2D(tmp, cv2.CV_32F, f))
    features = np.maximum(vertical, horizontal)

    # f = np.asarray([[-0.5, 0, 0, 0, 1, 0, 0, 0, -0.5]], dtype=np.float32)
    # tmp = np.maximum(cv2.filter2D(tmp, cv2.CV_32F, f.T), cv2.filter2D(tmp, cv2.CV_32F, f))

    # TODO smarter thresholding
    lines = np.where(features > 0.2, 255, 0).astype(np.uint8)

    # plt.imshow(lines)
    # plt.show()

    # apply field mask
    lines *= field_mask

    # remove artifacts
    lines[:, -4:] = 0

    # lines = cv2.morphologyEx(lines, cv2.MORPH_CLOSE, np.ones((3, 9), np.uint8))

    # remove screen marks
    # tmp[22:55, 44:328] = 0
    # tmp[35:55, 780:820] = 0
    # print(lines.dtype)
    return field_mask, lines


class FitFieldIndex:
    def __init__(self, path):
        dim = 576
        x = np.load(path)
        # self.index = AnnoyIndex(dim, 'angular')  # Length of item vector that will be indexed
        # self.index.load("index5.ann")

        self.orig = x["imgs"]
        self.imgs = x["imgs"].copy().astype(np.float32) / 255
        norms = np.maximum(norm(self.imgs), 1e-6)
        self.imgs /= norms[:, None]

        self.cfgs = x["cfgs"]

    def __call__(self, lines_img):
        size = 2
        f = cv2.resize(lines_img, (size * 16, size * 9), interpolation=cv2.INTER_AREA)
        # cv2.imshow("f", f)
        f = f.reshape(-1).astype(np.float32)
        f /= np.linalg.norm(f)

        # indices, distances = self.index.get_nns_by_vector(f, 10, include_distances=True)
        # print(distances)
        # return self.cfgs[indices],(1 - np.asarray(distances))
        scores = self.imgs.dot(f)
        ws = np.argsort(-scores)[:10]
        return self.cfgs[ws], scores[ws]


def icp_fitting(lines_img, camera, field, n_iter=5):
    image_points = cv2.findNonZero(lines_img).reshape(-1, 2)

    tree = cKDTree(image_points)

    projected_points = camera.project_points(field.get_points(2.0), remove_out_of_frame=True)
    projected_points = np.asarray(projected_points)

    h, w = lines_img.shape[:2]
    M = sensor_to_image_projection(w, h)
    projected_points = projected_points @ M.T

    M = np.eye(3, dtype=np.float32)
    for i in range(n_iter):
        distances, matches = tree.query(projected_points[:, :2], k=1, distance_upper_bound=50)
        mask = distances < 1e3
        distances = distances[mask]
        src = projected_points[mask][:, :2]
        dst = image_points[matches[mask]]

        mask = distances < 4 * np.quantile(distances, 0.5)
        src = src[mask]
        dst = dst[mask]

        # src = projected_points[mask][:, :2]
        # dst = image_points[matches[mask]]
        #
        # tmp = np.zeros((lines_img.shape[0], lines_img.shape[1], 3), dtype=np.uint8)
        # for i in range(3):
        #     tmp[:, :, i] = lines_img
        # for i in range(src.shape[0]):
        #     cv2.line(tmp, (int(src[i][0]), int(src[i][1])), (int(dst[i][0]), int(dst[i][1])), (255, 0, 0), 3)
        #
        # cv2.imshow("tmp", tmp)
        # cv2.waitKey(0)

        try:
            cM, _ = cv2.findHomography(src, dst)
        except:
            break
        if cM is None:
            break
        projected_points = projected_points @ cM.T
        projected_points /= projected_points[:, 2][:, None]
        M = cM @ M

    return M
