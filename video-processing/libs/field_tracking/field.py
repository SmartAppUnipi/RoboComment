import math

import numpy as np


def unroll_lines(points, lines):
    unrolled = []
    for g in lines.split(" "):
        for i in range(len(g) - 1):
            a = ord(g[i]) - ord('A')
            b = ord(g[i + 1]) - ord('A')
            unrolled.append(points[a])
            unrolled.append(points[b])

    return unrolled


def get_field_lines(w=105, h=68):
    ag = (h - 40.32) / 2
    ak = (h - 18.32) / 2

    points = [
        (0, 0),  # A
        (w / 2, 0),
        (w, 0),
        (w, h),
        (w / 2, h),
        (0, h),  # F
        (0, ag),
        (16.5, ag),
        (16.5, h - ag),
        (0, h - ag),  # J
        (0, ak),
        (5.5, ak),
        (5.5, h - ak),
        (0, h - ak),
        (w, ag),  # O
        (w - 16.5, ag),
        (w - 16.5, h - ag),
        (w - 0, h - ag),
        (w - 0, ak),  # T
        (w - 5.5, ak),
        (w - 5.5, h - ak),
        (w - 0, h - ak),
        (11.0, h / 2 - 0.06),
        (11.0, h / 2 + 0.06),
        (w - 11.0, h / 2 - 0.06),
        (w - 11.0, h / 2 + 0.06)
    ]

    lines = "ABCDEFA BE GHIJ KLMN OPQR STUV WX YZ"

    points = unroll_lines(points, lines)

    # add center circle
    steps = 24
    for i in range(steps):
        points.append((w / 2 + 9.15 * np.cos(np.pi * 2 * i / steps), h / 2 + 9.15 * np.sin(np.pi * 2 * i / steps)))
        points.append(
            (w / 2 + 9.15 * np.cos(np.pi * 2 * (i + 1) / steps), h / 2 + 9.15 * np.sin(np.pi * 2 * (i + 1) / steps)))

    steps = 8
    s_angle = -math.atan2(np.sqrt(9.15 ** 2 - 5.5 ** 2), 5.5)
    print(s_angle)
    angle_step = -2 * s_angle / steps
    for i in range(steps):
        angle = s_angle + i * angle_step
        points.append((11.0 + 9.15 * np.cos(angle), h / 2 + 9.15 * np.sin(angle)))
        points.append((11.0 + 9.15 * np.cos(angle + angle_step), h / 2 + 9.15 * np.sin(angle + angle_step)))

    for i in range(steps):
        angle = s_angle + i * angle_step
        points.append((w - 11.0 - 9.15 * np.cos(angle), h / 2 + 9.15 * np.sin(angle)))
        points.append((w - 11.0 - 9.15 * np.cos(angle + angle_step), h / 2 + 9.15 * np.sin(angle + angle_step)))

    return points


def lines_to_points(lines, spacing=1.0):
    lines = np.asarray(lines, dtype=np.float32)
    points = []
    for i in range(0, len(lines), 2):
        v = lines[i + 1] - lines[i]
        d = np.linalg.norm(v)
        points.append(lines[i])
        points.append(lines[i + 1])
        if d > spacing:
            steps = int(d / spacing)
            for j in range(steps):
                points.append(lines[i] + v * (j + 1) / steps)

    return np.unique(np.asarray(points, dtype=np.float32), axis=0)


class SoccerField:
    def __init__(self, width=105.0, height=68.0):
        """
        :param width: In meters
        :param height: In meters
        """
        self.w = width
        self.h = height

        self.lines = get_field_lines()

    def get_points(self, spacing=1.0):
        return lines_to_points(self.lines, spacing)

    def svg(self, circles, scale=6):
        """
        Create an SVG image of the field
        :param circles: [(x, y, color, radius)]
        :param scale:
        :return:
        """
        pad = 15
        code = []
        code.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{int(scale * self.w + 2 * pad + 1)}' "
                    f"height='{int(scale * self.h + 2 * pad + 1)}'>\n")
        code.append("<rect width='100%' height='100%' fill='green'/>")

        lines = np.asarray(self.lines, dtype=np.float32)
        for i in range(0, len(self.lines), 2):
            sx, sy = lines[i] * scale + pad
            ex, ey = lines[i + 1] * scale + pad
            code.append(f"<line x1='{sx}' y1='{sy}' x2='{ex}' y2='{ey}' stroke='white' stroke-width='1' />")

        for x, y, color, r, txt in circles:
            y = self.h - y
            code.append(f"<circle cx='{x * scale + pad}' cy='{y * scale + pad}' r='{r * scale}' fill='{color}'/>")
            if txt:
                code.append(f"<text x='{x * scale + pad}' y='{(y+r/2) * scale + pad}' text-anchor='middle'>{txt}</text>")

        code.append("</svg>")

        return "".join(code)
