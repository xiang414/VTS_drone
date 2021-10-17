import cv2
import numpy as np
import sys
import time

def nothing(x):
    pass
fps_time = time.time()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cv2.namedWindow('hsv_tune',cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow("hsv_tune", 640, 480)
cv2.createTrackbar('hl', 'hsv_tune', 0,   179, nothing)
cv2.createTrackbar('hu', 'hsv_tune', 179, 179, nothing)
cv2.createTrackbar('sl', 'hsv_tune', 0,   255, nothing)
cv2.createTrackbar('su', 'hsv_tune', 255, 255, nothing)
cv2.createTrackbar('vl', 'hsv_tune', 0,   255, nothing)
cv2.createTrackbar('vu', 'hsv_tune', 255, 255, nothing)
while(True):
    frame = cv2.imread(r'..\img\led18.jpg')
    #ret , frame = cap.read()
    """
    if time.time()-fps_time>0:
        fps = int(1/(time.time()-fps_time))
        fps_time = time.time()
    else:
		fps=0
    #fps = cv2.cv.CV_CAP_PROP_FPS
    print 'FPS = ' , fps
    """
    h, s, v = 100, 100, 100
    hl = cv2.getTrackbarPos('hl', 'hsv_tune')
    hu = cv2.getTrackbarPos('hu', 'hsv_tune')
    sl = cv2.getTrackbarPos('sl', 'hsv_tune')
    su = cv2.getTrackbarPos('su', 'hsv_tune')
    vl = cv2.getTrackbarPos('vl', 'hsv_tune')
    vu = cv2.getTrackbarPos('vu', 'hsv_tune')
    kernel = np.ones((5,5),np.uint8)
    
    #blur = frame
    blur = cv2.GaussianBlur(frame,(5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower = np.array([hl, sl, vl])
    upper = np.array([hu, su, vu])

    mask = cv2.inRange(hsv, lower, upper)
    #blur = cv2.medianBlur(mask,5)
    mask = cv2.dilate(mask, kernel, iterations=3)
    result = cv2.bitwise_and(blur, blur, mask=mask)
    cv2.imshow("hsv_tune", result)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cap.release()
        break

cv2.destroyAllWindows()
