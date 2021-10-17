# -*- coding: utf-8 -*-
"""
Created on Thu May  2 20:55:00 2019

@author: enjoy
"""
import cv2
import numpy as np
import math
from os import mkdir
from os.path import isdir
#import statistics as sta

if not isdir(r'..\img\find_circle'):
    mkdir(r'..\img\find_circle')

image = cv2.imread(r'..\img\led18.jpg')
image = cv2.resize(image,(640,480),interpolation=cv2.INTER_CUBIC)
cv2.imwrite(r'..\img\find_circle\resize_img.jpg',image)
blur = cv2.GaussianBlur(image,(9,9),0)
#blur = image
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
cv2.imwrite(r'..\img\find_circle\hsv_img.jpg',hsv)
kernel = np.ones((9,9),np.uint8)
kernel1 = np.ones((3,3),np.uint8)  
#red_lower = np.array([90 , 135 , 0])
#red_upper = np.array([150 , 255 , 255])
blue_lower = np.array([100 , 145 , 90])
blue_upper = np.array([155 , 255 , 255])
#red_lower = np.array([145 , 120 , 110])
#red_upper = np.array([179 , 255 , 255])
red_lower = np.array([135 , 70 , 90])
red_upper = np.array([179 , 255 , 255])
red_binary = cv2.inRange(hsv, red_lower, red_upper)
cv2.imwrite(r'..\img\find_circle\red_binary.jpg',red_binary)
blue_binary = cv2.inRange(hsv, blue_lower, blue_upper)
cv2.imwrite(r'..\img\find_circle\blue_binary.jpg',blue_binary)
red_blur = cv2.medianBlur(red_binary,5)
blue_blur = cv2.medianBlur(blue_binary,5)
cv2.imwrite(r'..\img\find_circle\red_blur.jpg',red_blur)
cv2.imwrite(r'..\img\find_circle\blue_blur.jpg',blue_blur)
red_erode = cv2.erode(red_blur , kernel1 , iterations=2)
red_dilate = cv2.dilate(red_blur, kernel, iterations=4)
cv2.imwrite(r'..\img\find_circle\red_dilate.jpg',red_dilate)
blue_dilate = cv2.dilate(blue_blur, kernel, iterations=4)
red_contours, _ = cv2.findContours(red_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
blue_contours, _ = cv2.findContours(blue_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
add = cv2.add(red_dilate,blue_dilate)
cv2.imwrite(r'..\img\find_circle\add_img.jpg',add)
cv2.imshow('add' , add)
cv2.waitKey(0)
'''
cv2.imshow('blue_blur' , blue_blur)
cv2.waitKey(0)
cv2.imshow('red_blur' , red_blur)
cv2.waitKey(0)
cv2.imshow('blue_dilate' , blue_dilate)
cv2.waitKey(0)
cv2.imshow('red_dilate' , red_dilate)
cv2.waitKey(0)
cv2.imshow('add' , add)
cv2.waitKey(0)
'''
#blue = add - red_dilate
#red = add - blue_dilate

#"""新方法
check = cv2.bitwise_and(red_dilate, blue_dilate)
cv2.imshow('check' , check)
cv2.waitKey(0)
cv2.imwrite(r'..\img\find_circle\check.jpg',check)
check_contours, _ = cv2.findContours(check, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
check_cnt = check_contours[0]
check_M = cv2.moments(check_cnt)
x_check = int(check_M["m10"] / check_M["m00"])
y_check = int(check_M["m01"] / check_M["m00"])
check_center = (x_check,y_check)
#cv2.circle(image, check_center, 5, (0, 255, 0), -1)
#cv2.drawContours(image, check_contours, -1, (0,255,255), 1)
#cv2.imshow('check_1' , image)
# cv2.imwrite(r'..\img\find_circle\check_1.jpg',image)
#cv2.waitKey(0)
add_contours, _ = cv2.findContours(add, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(add_contours)):
    dist = cv2.pointPolygonTest(add_contours[i],check_center,False)
    if dist > 0:
        actual = i
#cv2.drawContours(image, add_contours, -1, (0,255,255), 1)
# cv2.imwrite(r'..\img\find_circle\check_2.jpg',image)
# cv2.imshow('check' , image)
# cv2.waitKey(0)
for i in range(len(red_contours)):
    red_cnt = red_contours[i]
    red_M = cv2.moments(red_cnt)
    x_red = int(red_M["m10"] / red_M["m00"])
    y_red = int(red_M["m01"] / red_M["m00"])
    red_center = (int(red_M["m10"] / red_M["m00"]), int(red_M["m01"] / red_M["m00"]))
    dist_red = cv2.pointPolygonTest(add_contours[actual],red_center,False)
    if dist_red > 0:
        red_actual = i
        red_point = red_center
cv2.drawContours(image, red_contours, red_actual, (0,255,255), 1)
cv2.circle(image, red_point, 5, (0, 255, 0), -1)
print(red_point)
cv2.imwrite(r'..\img\find_circle\result.jpg',image)
#"""

"""舊方法
s_list = []
red_contours, _ = cv2.findContours(red_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(red_contours)):
    data_list = []
    red_cnt = red_contours[i]
    epsilon = 0.01*cv2.arcLength(red_cnt,True)
    approx = cv2.approxPolyDP(red_cnt,epsilon,True)
    red_M = cv2.moments(red_cnt)
    #red_center = (int(red_M["m10"] / red_M["m00"]), int(red_M["m01"] / red_M["m00"]))
    x = int(red_M["m10"] / red_M["m00"])
    y = int(red_M["m01"] / red_M["m00"])
    center = (x,y)
    cv2.circle(red_dilate, center, 5, (0, 255, 0), -1)
    for j in range(len(approx)):
        #length = int(math.sqrt((approx[j][0][0] - x)**2 + (approx[j][0][1] - y)**2))
        contour_point = (approx[j][0][0],approx[j][0][1])
        length = int(math.sqrt((approx[j][0][0] - x)**2 + (approx[j][0][1] - y)**2))
        cv2.line(red_dilate, center, contour_point, (0, 0, 255), 2)
        data_list.append(length)
    s = np.std(data_list)
    s_list.append(s)
    #print s
    print (data_list)
    #cv2.circle(blur, red_center, 5, (0, 255, 0), -1)
    #cv2.drawContours(blur, [approx], -1, (0,255,255), 1)
    area = cv2.contourArea(approx)
    #print 'red area:' , area
   # print 'red contours:' , approx[1][0][1]
#print math.sin((240*np.pi)/180)
m = np.where(s_list==np.min(s_list))
print (s_list , m[0][0])
a = m[0][0]
i=0
red_cnt = red_contours[a]
area = cv2.contourArea(red_cnt)
print(area)

#red_cnt = max(red_contours,key=cv2.contourArea)
#red_M = cv2.moments(red_cnt)
#red_cnt = max(red_contours,key=cv2.contourArea)
epsilon = 0.01*cv2.arcLength(red_cnt,True)
approx = cv2.approxPolyDP(red_cnt,epsilon,True)
red_center = (int(red_M["m10"] / red_M["m00"]), int(red_M["m01"] / red_M["m00"]))
cv2.circle(blur, red_center, 5, (0, 255, 0), -1)
cv2.drawContours(image, red_contours, a, (0,255,255), 2)
cv2.imwrite('line.jpg',red_dilate)
#"""
#cv2.imshow('red_erode' , red_erode)
#cv2.waitKey(0)
cv2.imshow('red' , red_dilate)
cv2.waitKey(0)
cv2.imshow('image' , image)
cv2.waitKey(0)
cv2.destroyAllWindows()