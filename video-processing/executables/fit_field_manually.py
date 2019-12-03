import cv2
from libs.field_tracking.camera import Camera, draw_lines
from libs.field_tracking.field import SoccerField

cap = cv2.VideoCapture("videos/gonzalo_goal.mp4")
for i in range(400):
    ret, frame = cap.read()

frame = cv2.resize(frame, (60 * 16, 60 * 9))

print(frame.shape)

# get field polygon
field = SoccerField()

dx = 22.0  # field.w / 2
dy = 30.0  # field.h / 2
f = 5.0

camera = Camera([field.w / 2, -32.5, 14], [dx, dy, 0], f)

while True:
    lines = camera.project_lines(field.lines)
    img = draw_lines(frame.copy(), lines, 255, 3)

    cv2.imshow("img", img)
    if not camera.apply_key(cv2.waitKey(0)):
        break
