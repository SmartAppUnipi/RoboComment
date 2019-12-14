import numpy as np
import cv2


def lookat_matrix(camera_pos, look_at, up=(0, 0, 1)):
    camera_pos = np.asarray(camera_pos)
    look_at = np.asarray(look_at)
    up = np.asarray(up)

    f = look_at - camera_pos
    f /= np.linalg.norm(f)
    l = np.cross(up, f)
    l /= np.linalg.norm(l)
    u = np.cross(f, l)

    R = np.eye(4, dtype=np.float32)
    R[0, :3] = l
    R[1, :3] = u
    R[2, :3] = f

    T = np.eye(4, dtype=np.float32)
    T[:3, 3] = -camera_pos

    return R @ T


def to_3d_homogeneous(x):
    x = np.asarray(x, dtype=np.float32)

    if x.shape[1] == 2:
        return np.hstack((x, np.zeros((x.shape[0], 1)), np.ones((x.shape[0], 1))))

    if x.shape[1] == 3:
        return np.hstack((x, np.ones((x.shape[0], 1))))

    return x


def to_2d_homogeneous(x):
    x = np.asarray(x, dtype=np.float32)

    if x.shape[1] == 2:
        return np.hstack((x, np.ones((x.shape[0], 1))))

    return x


def project_points(points, M):
    if M.shape == (3, 4):
        points = to_3d_homogeneous(points)
    elif M.shape == (3, 3):
        points = to_2d_homogeneous(points)
    else:
        raise Exception("Wrong projection matrix shape, got", M.shape, "expect (3, 4) or (3, 3)")
    return points @ M.T


def project_lines(lines, M, near_clip=0.01):
    cp = project_points(lines, M)
    clipped = []

    for i in range(0, len(cp), 2):
        v = cp[i + 1] - cp[i]
        alphas = 0.0
        alphae = 1.0

        if abs(v[2]) > 1e-6:
            s = (near_clip - cp[i][2]) / v[2]

            if v[2] > 0:
                alphas = max(alphas, s)
            if v[2] < 0:
                alphae = min(alphae, s)
        else:
            alphae = float(cp[i, 2] > near_clip)

        if alphas < alphae:
            cp[i] += alphas * v
            cp[i + 1] = cp[i] + alphae * v

            cp[i] /= cp[i][2]
            cp[i + 1] /= cp[i + 1][2]

            clipped.append(cp[i])
            clipped.append(cp[i + 1])

    return clipped


class Camera:
    def __init__(self, camera_position, look_at, zoom_level):
        self.move(camera_position, look_at, zoom_level)

    def move(self, camera_position, look_at, zoom_level):
        self.camera_position = np.asarray(camera_position)
        self.look_at = np.asarray(look_at)
        self.zoom_level = zoom_level

        # camera matrix
        C = lookat_matrix(camera_position, look_at)

        # perspective projection matrix
        P = np.asarray([[-zoom_level, 0, 0, 0], [0, -zoom_level, 0, 0], [0, 0, 1, 0]], dtype=np.float32)

        self.M = P @ C

    def apply_key(self, key):
        print(key)
        if key == 56:
            self.camera_position += [0, 0.5, 0]
        if key == 50:
            self.camera_position -= [0, 0.5, 0]
        if key == 52:
            self.camera_position -= [0.5, 0, 0]
        if key == 54:
            self.camera_position += [0.5, 0, 0]
        if key == 57:
            self.camera_position += [0, 0, 0.5]
        if key == 51:
            self.camera_position -= [0, 0, 0.5]

        if key == 97:
            self.look_at -= [0.5, 0, 0]
        if key == 100:
            self.look_at += [0.5, 0, 0]
        if key == 115:
            self.look_at -= [0, 0.5, 0]
        if key == 119:
            self.look_at += [0, 0.5, 0]

        if key == 43:
            self.zoom_level += 0.1
        if key == 45:
            self.zoom_level -= 0.1

        if key == 27:
            return False

        print(self.camera_position, self.look_at, self.zoom_level)
        self.move(self.camera_position, self.look_at, self.zoom_level)
        return True

    def get_homography(self, w, h):
        return sensor_to_image_projection(w, h) @ self.M[:, (0, 1, 3)]

    def project_lines(self, lines, near_clip=0.01):
        return project_lines(lines, self.M, near_clip)

    def project_points(self, points, near_clip=0.01, remove_out_of_frame=False):
        cp = project_points(points, self.M)
        projected = []
        for p in cp:
            if p[2] >= near_clip:
                p /= p[2]
                if not remove_out_of_frame or (-1 <= p[0] <= 1 and -1 <= p[1] <= 1):
                    projected.append(p)

        return projected


def sensor_to_image_projection(w, h):
    """
    Transformation that projects points from sensor space (-1, 1) x (-1, 1) to an image of size (w, h)
    :param w:
    :param h:
    :return: The transformation (a 3x3 matrix)
    """
    s = max(h, w) / 2

    return np.asarray([
        [s, 0, w / 2],
        [0, s, h / 2],
        [0, 0, 1]
    ], dtype=np.float32)


def _create_image_if_tuple(img, color):
    if isinstance(img, tuple):
        shape = img + (3,) if isinstance(color, tuple) else img
        img = np.zeros(shape, dtype=np.uint8)

    return img


def draw_lines(img, lines, color=(255, 255, 255), width=1, requires_scaling=True):
    """
    Draw multiple lines
    :param img: An image or a tuple (height, width)
    :param lines: An 2D array of points, they will be connected as AB CD EF...
    :param color:
    :param width:
    :param requires_scaling:
    :return: the image
    """
    img = _create_image_if_tuple(img, color)

    if requires_scaling:
        h, w = img.shape[:2]
        M = sensor_to_image_projection(w, h)
        lines = lines @ M.T

    for i in range(0, len(lines), 2):
        a = np.round(lines[i]).astype(np.int32)
        b = np.round(lines[i + 1]).astype(np.int32)

        cv2.line(img, (a[0], a[1]), (b[0], b[1]), color, width)

    return img


def draw_points(img, points, color=(255, 255, 255), radius=1):
    """
    :param img: An image or a tuple (height, width)
    :param points: An 2D array of points, they will be connected as AB CD EF...
    :param color:
    :param radius:
    :return: the image
    """
    img = _create_image_if_tuple(img, color)

    h, w = img.shape[:2]
    M = sensor_to_image_projection(w, h)
    points = points @ M.T

    for p in points:
        a = np.round(p).astype(np.int32)

        cv2.circle(img, (a[0], a[1]), radius, color, thickness=-1)

    return img
