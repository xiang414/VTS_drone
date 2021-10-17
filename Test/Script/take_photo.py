import cv2
import numpy as np
import time
from os import mkdir
from os.path import isdir

def nothing(x):
    pass

if not isdir(r'..\img\take_photo'):
    mkdir(r'..\img\take_photo')

cap = cv2.VideoCapture(0)
w = cap.get(3)
h = cap.get(4)
print(w,h)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ret=cap.set(3,640)
ret=cap.set(4,480)
cv2.namedWindow('take_photo')
center = (320 , 240)
while(True):
    ret, frame = cap.read()
    cv2.circle(frame, center, 5, (0, 0, 0), -1)
    cv2.imshow("take_photo", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
       cv2.imwrite(r'..\img\take_photo\led15.png',frame)
       break

cv2.destroyAllWindows()