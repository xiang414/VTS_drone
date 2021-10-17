# -*- coding: utf-8 -*-
"""
python 3.7.3
OpenCV 3.4.0
"""
import cv2
import numpy as np
import sys
import math
import socket
import time
import PID
#---------------------------Setup---------------------------
takeoff = 0
timer = 0
erode_flag = 0  
stop_timer = 0
stop_time = 0
up_timer = 0
up_time = 0
up = 0
fps_time = time.perf_counter()
tello_address = ('192.168.8.102', 8889)
local_address = ('192.168.0.100', 8889)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_address)
cap = cv2.VideoCapture(0)
data_list = []
error_list = []
red_hl , red_sl , red_vl = 130,90,90
red_hu , red_su , red_vu = 179,255,255
blue_hl , blue_sl , blue_vl = 100,145,90
blue_hu , blue_su , blue_vu = 155,255,255
P = 0.14
I = 0.12
D = 0.14
pid = PID.PID(P, I, D)
pid.SetPoint = 0.0
pid.setSampleTime(0.0)
pid.setWindup(30.0)
yaw_P = 0.0
yaw_I = 0.0
yaw_D = 0.0
yaw_pid = PID.PID(yaw_P,yaw_I,yaw_D)
yaw_pid.setSampleTime(0.0)
yaw_pid.setWindup(10.0)
#---------------------------Tello_Receive_Command---------------------------
def receive():#接收Tello回傳訊息，本程式中沒有使用此功能
    while True:
        try:
          response, ip_address = sock.recvfrom(128)
          print("Received message: " + response.decode(encoding='utf-8'))
          return response.decode(encoding='utf-8')
        except Exception as e:
          sock.close()
          print("Error receiving: " + str(e))
          break
#---------------------------Control_Tello---------------------------
def Control_Tello(message):#送SDK Command
    try:
        sock.sendto(message.encode(), tello_address)
        print("Sending message: " + message)
        data_list.append(message)
    except Exception as e:
        print("Error sending: " + str(e))
#---------------------------Get_Red_Led---------------------------
def RedHSV(hsv , hl , sl , vl , hu , su , vu , erode_flag):#閥值處理後得到紅色LED的二值化影像
    kernel = np.ones((9,9),np.uint8)
    kernel1 = np.ones((3,3),np.uint8)
    red_lower = np.array([hl , sl , vl])
    red_upper = np.array([hu , su , vu])
    red_binary = cv2.inRange(hsv, red_lower, red_upper)
    red_blur = cv2.medianBlur(red_binary,5)   #11
    #red_erode = cv2.erode(red_blur,kernel1,iterations=2)
    red_dilate = cv2.dilate(red_blur,kernel,iterations=4)
    return red_dilate
#---------------------------Get_Blue_Led---------------------------
def BlueHSV(hsv , hl , sl , vl , hu , su , vu , erode_flag):#閥值處理後得到藍色LED的二值化影像
    kernel = np.ones((9,9),np.uint8)
    kernel1 = np.ones((3,3),np.uint8)
    blue_lower = np.array([hl , sl , vl])
    blue_upper = np.array([hu , su , vu])
    blue_binary = cv2.inRange(hsv, blue_lower, blue_upper)
    blue_blur = cv2.medianBlur(blue_binary,5)
    #blue_erode = cv2.erode(blue_blur,kernel1,iterations=2)
    blue_dilate = cv2.dilate(blue_blur,kernel,iterations=4)
    return blue_dilate
#---------------------------Check_contours---------------------------
def Check_contours(red , blue):#檢查是否為Tello上的紅色藍色LED燈
    add = cv2.add(red,blue)
    check = cv2.bitwise_and(red, blue)
    (_,check_contours,_) = cv2.findContours(check,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    try:
        check_cnt = check_contours[0]
        check_M = cv2.moments(check_cnt)
        x_check = int(check_M["m10"] / check_M["m00"])
        y_check = int(check_M["m01"] / check_M["m00"])
        check_center = (x_check,y_check)
        (_,add_contours,_) = cv2.findContours(add,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(add_contours)):
            dist = cv2.pointPolygonTest(add_contours[i],check_center,False)
            if dist > 0:
                actual = i
        return add_contours[actual]
    except:
        return 'error'
        print("check_error")
#---------------------------Find_Red_Led_Coordinate---------------------------
def Red_contours(red_binary_img,blue_binary_img):
    s_list = []
    (_,red_contours, _) = cv2.findContours(red_binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    try:
        print('Red contours:' , len(red_contours))
        check = Check_contours(red_binary_img,blue_binary_img)
        if check != 'error':
            if len(red_contours) > 1:
                actual_contours = Check_contours(red_binary_img,blue_binary_img)
                for i in range(len(red_contours)):
                    red_cnt = red_contours[i]
                    red_M = cv2.moments(red_cnt)
                    x_red = int(red_M["m10"] / red_M["m00"])
                    y_red = int(red_M["m01"] / red_M["m00"])
                    red_center = (int(red_M["m10"] / red_M["m00"]), int(red_M["m01"] / red_M["m00"]))
                    dist_red = cv2.pointPolygonTest(actual_contours,red_center,False)
                    if dist_red > 0:
                        red_actual = i
                        red_point = red_center
                cv2.drawContours(frame, red_contours, red_actual, (0,255,255), 2)
                cv2.circle(frame, red_point, 5, (0, 0, 0), -1)
                return red_point[0] , red_point[1]
            elif len(red_contours) == 1:
                red_cnt = red_contours[0]
                red_M = cv2.moments(red_cnt)
                x = int(red_M["m10"] / red_M["m00"])
                y = int(red_M["m01"] / red_M["m00"])
                red_center = (x,y)
                cv2.drawContours(frame, red_contours, -1, (0,255,0), 2)
                cv2.circle(frame, red_center, 5, (0, 0, 0), -1)
                return x , y
        else:
            print("Can't detect Red light")
    except:
        try:
            for i in range(len(red_contours)):
                data_list = []
                red_cnt = red_contours[i]
                epsilon = 0.01*cv2.arcLength(red_cnt,True)
                approx = cv2.approxPolyDP(red_cnt,epsilon,True)
                red_M = cv2.moments(red_cnt)
                x = int(red_M["m10"] / red_M["m00"])
                y = int(red_M["m01"] / red_M["m00"])
                for j in range(len(approx)):
                    length = int(math.sqrt((approx[j][0][0] - x)**2 + (approx[j][0][1] - y)**2))
                    data_list.append(length)
                s = np.std(data_list)
                s_list.append(s)
            m = np.where(s_list==np.min(s_list))
            a = m[0][0]
            red_cnt = red_contours[a]
            red_M = cv2.moments(red_cnt)
            x = int(red_M["m10"] / red_M["m00"])
            y = int(red_M["m01"] / red_M["m00"])
            red_center = (x,y)
            cv2.circle(frame, red_center, 5, (0, 255, 0), -1)
            cv2.drawContours(frame, red_contours, a, (0,0,255), 2)
            return x , y
        except:
            print("Red error:", sys.exc_info()[0])
#---------------------------Find_Blue_Led_Coordinate---------------------------
def Blue_contours(red_binary_img,blue_binary_img):
    s_list = []
    (_,blue_contours, _) = cv2.findContours(blue_binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    try:
        print('Blue contours:' , len(blue_contours))
        check = Check_contours(red_binary_img,blue_binary_img)
        if check != 'error':
            if len(blue_contours) > 1:
                actual_contours = Check_contours(red_binary_img,blue_binary_img)
                for i in range(len(blue_contours)):
                    blue_cnt = blue_contours[i]
                    blue_M = cv2.moments(blue_cnt)
                    x_blue = int(blue_M["m10"] / blue_M["m00"])
                    y_blue = int(blue_M["m01"] / blue_M["m00"])
                    blue_center = (x_blue,y_blue)
                    dist_blue = cv2.pointPolygonTest(actual_contours,blue_center,False)
                    if dist_blue > 0:
                        blue_actual = i
                        blue_point = blue_center
                cv2.drawContours(frame, blue_contours, blue_actual, (0,255,255), 2)
                cv2.circle(frame, blue_point, 5, (0, 0, 0), -1)
                return blue_point[0] , blue_point[1]
            elif len(blue_contours) == 1:
                blue_cnt = blue_contours[0]
                blue_M = cv2.moments(blue_cnt)
                x = int(blue_M["m10"] / blue_M["m00"])
                y = int(blue_M["m01"] / blue_M["m00"])
                blue_center = (x,y)
                cv2.drawContours(frame, blue_contours, -1, (0,255,0), 2)
                cv2.circle(frame, blue_center, 5, (0, 0, 0), -1)
                return x , y
        else:
            print("Can't detect Blue light")
    except:
        try:
            for i in range(len(blue_contours)):
                data_list = []
                blue_cnt = blue_contours[i]
                epsilon = 0.01*cv2.arcLength(blue_cnt,True)
                approx = cv2.approxPolyDP(blue_cnt,epsilon,True)
                blue_M = cv2.moments(blue_cnt)
                x = int(blue_M["m10"] / blue_M["m00"])
                y = int(blue_M["m01"] / blue_M["m00"])
                for j in range(len(approx)):
                    length = int(math.sqrt((approx[j][0][0] - x)**2 + (approx[j][0][1] - y)**2))
                    data_list.append(length)
                s = np.std(data_list)
                s_list.append(s)
            m = np.where(s_list==np.min(s_list))
            a = m[0][0]
            blue_cnt = blue_contours[a]
            blue_M = cv2.moments(blue_cnt)
            x = int(blue_M["m10"] / blue_M["m00"])
            y = int(blue_M["m01"] / blue_M["m00"])
            red_center = (x,y)
            cv2.circle(frame, red_center, 5, (0, 255, 0), -1)
            cv2.drawContours(frame, blue_contours, a, (0,0,255), 2)
            return x , y
        except:
            print("Blue error:", sys.exc_info()[0])
#---------------------------Find_two_led_angle_and_led_to_imgcenter_angle---------------------------
def Angle(red_x , blue_x , red_y , blue_y , two_point_center_x , two_point_center_y):
    led_point_x = red_x - blue_x
    led_point_y = red_y - blue_y
    two_led_angle = math.atan2(led_point_y , led_point_x)
    led_to_imgcenter_x = two_point_center_x - 320
    led_to_imgcenter_y = two_point_center_y - 240
    led_to_imgcenter_angle = math.atan2(led_to_imgcenter_y , led_to_imgcenter_x)
    return two_led_angle , led_to_imgcenter_angle
#---------------------------True_Two_Led_Angle---------------------------
def Modulated_Two_Led_Angle(red_y , two_point_center_y , two_led_angle):
    if two_point_center_y - red_y >= 0 :
        modulated_two_led_angle = abs(two_led_angle*(180/np.pi))
    elif red_y - two_point_center_y >= 0 :
        modulated_two_led_angle = 360 - two_led_angle*(180/np.pi)
    else :
        print('not defined')
    return modulated_two_led_angle
#---------------------------True_Led_To_Imgcenter_Angle---------------------------
def Modulated_Led_To_Imgcenter_Angle(two_point_center_y , led_to_imgcenter_angle):
    if 240 - two_point_center_y >= 0 :
        modulated_led_to_imgcenter_angle = abs(led_to_imgcenter_angle*(180/np.pi))
    elif two_point_center_y - 240 >= 0 :
        modulated_led_to_imgcenter_angle = 360 - led_to_imgcenter_angle*(180/np.pi)
    else :
        print('not defined')
    return modulated_led_to_imgcenter_angle
#---------------------------RC---------------------------
def RC(led_angle , center_angle , time):
    try:
        a = math.cos((center_angle*np.pi)/180)
        b = math.sin((center_angle*np.pi)/180)
        a10 = abs(int(time*a))
        b10 = abs(int(time*b))
        if center_angle >= 0 and center_angle <= 90:
            if led_angle >= 45 and led_angle <= 135:
                roll = a10
                pitch = -b10
                yaw_pid.SetPoint = 90.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 90:
                    yaw = -yaw
            elif led_angle >= 135 and led_angle <= 225:
                roll = b10
                pitch = a10
                yaw_pid.SetPoint = 180.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 180:
                    yaw = -yaw
            elif led_angle >= 225 and led_angle <= 315:
                roll = -a10
                pitch = b10
                yaw_pid.SetPoint = 270.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 270:
                    yaw = -yaw
            elif led_angle >= 315 and led_angle <= 360:
                roll = -b10
                pitch = -a10
                yaw_pid.SetPoint = 360.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 360:
                    yaw = -yaw
            elif led_angle >= 0 and led_angle <= 45:
                roll = -b10
                pitch = -a10
                yaw_pid.SetPoint = 0.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
        elif center_angle >= 90 and center_angle <= 180:
            if led_angle >= 45 and led_angle <= 135:
                roll = -a10
                pitch = -b10
                yaw_pid.SetPoint = 90.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 90:
                    yaw = -yaw
            elif led_angle >= 135 and led_angle <= 225:
                roll = b10
                pitch = -a10
                yaw_pid.SetPoint = 180.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 180:
                    yaw = -yaw
            elif led_angle >= 225 and led_angle <= 315:
                roll = a10
                pitch = b10
                yaw_pid.SetPoint = 270.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 270:
                    yaw = -yaw
            elif led_angle >= 315 and led_angle <= 360:
                roll = -b10
                pitch = a10
                yaw_pid.SetPoint = 360.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 360:
                    yaw = -yaw
            elif led_angle >= 0 and led_angle <= 45:
                roll = -b10
                pitch = a10
                yaw_pid.SetPoint = 0.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
        elif center_angle >= 180 and center_angle <= 270:
            if led_angle >= 45 and led_angle <= 135:
                roll = -a10
                pitch = b10
                yaw_pid.SetPoint = 90.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 90:
                    yaw = -yaw
            elif led_angle >= 135 and led_angle <= 225:
                roll = -b10
                pitch = -a10
                yaw_pid.SetPoint = 180.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 180:
                    yaw = -yaw
            elif led_angle >= 225 and led_angle <= 315:
                roll = a10
                pitch = -b10
                yaw_pid.SetPoint = 270.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 270:
                    yaw = -yaw
            elif led_angle >= 315 and led_angle <= 360:
                roll = b10
                pitch = a10
                yaw_pid.SetPoint = 360.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 360:
                    yaw = -yaw
            elif led_angle >= 0 and led_angle <= 45:
                roll = b10
                pitch = a10
                yaw_pid.SetPoint = 0.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
        elif center_angle >= 270 and center_angle <= 360:
            if led_angle >= 45 and led_angle <= 135:
                roll = a10
                pitch = b10
                yaw_pid.SetPoint = 90.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 90:
                    yaw = -yaw
            elif led_angle >= 135 and led_angle <= 225:
                roll = -b10
                pitch = a10
                yaw_pid.SetPoint = 180.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 180:
                    yaw = -yaw
            elif led_angle >= 225 and led_angle <= 315:
                roll = -a10
                pitch = -b10
                yaw_pid.SetPoint = 270.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 270:
                    yaw = -yaw
            elif led_angle >= 315 and led_angle <= 360:
                roll = b10
                pitch = -a10
                yaw_pid.SetPoint = 360.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
                if led_angle < 360:
                    yaw = -yaw
            elif led_angle >= 0 and led_angle <= 45:
                roll = b10
                pitch = -a10
                yaw_pid.SetPoint = 0.0
                yaw_pid.update(led_angle)
                yaw = abs(int(yaw_pid.output))
        else:
            roll , pitch , yaw = 0
        return roll , pitch , yaw
    except:
        print("Unexpected error:", sys.exc_info()[0])
#---------------------------Main.py---------------------------
while True:
    try:
        stop_time = time.perf_counter()
        up_time = time.perf_counter()
        if takeoff == 0 :
            Control_Tello("command")
            time.sleep(1)
            Control_Tello("rc 0 0 0 0")   
            time.sleep(2)
            Control_Tello("takeoff")
            time.sleep(2)
            Control_Tello("rc 0 0 20 0")
            time.sleep(1)
            takeoff = 1
        ret, frame = cap.read()
        if time.perf_counter() - fps_time > 0:
            fps = int(1/(time.perf_counter() - fps_time))
            fps_time = time.perf_counter()
        else:
            fps = 0
        print('FPS = ' , fps)
        blur = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        new_list = []
        red_edge = RedHSV(hsv,red_hl,red_sl,red_vl,red_hu,red_su,red_vu,erode_flag)
        #cv2.imshow("red_blur",red_edge)
        blue_edge = BlueHSV(hsv,blue_hl,blue_sl,blue_vl,blue_hu,blue_su,blue_vu,erode_flag)
        #cv2.imshow("blue_blur",blue_edge)
        try:
            red_x , red_y = Red_contours(red_edge,blue_edge)
            red_tuple = (red_x,red_y)
            new_list.append(red_tuple)
            blue_x , blue_y = Blue_contours(red_edge,blue_edge)
            blue_tuple = (blue_x,blue_y)
            new_list.append(blue_tuple)
            cv2.line(frame, new_list[0], new_list[1], (0, 0, 255), 3)
            two_point_center_x = (new_list[0][0] + new_list[1][0])/2
            two_point_center_y = (new_list[0][1] + new_list[1][1])/2
            two_point_center = (int(two_point_center_x),int(two_point_center_y))
            set_point = (320,240)
            cv2.circle(frame, two_point_center, 5, (0, 0, 0), -1)
            cv2.circle(frame, set_point, 5, (0, 0, 0), -1)
            two_led_length = int(math.sqrt((red_x - blue_x)**2 + (red_y - blue_y)**2))
            distance = int(math.sqrt((two_point_center_x - 320)**2 + (two_point_center_y - 240)**2))
            up = 0
            if two_led_length >= 40:
                pid.setKp(0.075)
                pid.setKi(0.2)
                pid.setKd(0.05)
                yaw_pid.setKp(0.05)
                yaw_pid.setKi(0.2)
                yaw_pid.setKd(0.0)
            else:
                pid.setKp(0.12)#0.12
                pid.setKi(0.15)
                pid.setKd(0.13)#0.13
                yaw_pid.setKp(0.06)
                yaw_pid.setKi(0.0)
                yaw_pid.setKd(0.0)
            if two_led_length >= 20 and two_led_length <= 80:
                red_hl_scale = 15/60.0
                red_sl_scale = 40/60.0
                red_vl_scale = 20/60.0
                red_hl = 135 + int((two_led_length - 20)*red_hl_scale)#135
                red_sl = 90 + int((two_led_length - 20)*red_sl_scale)#90
                red_vl = 90 + int((two_led_length - 20)*red_vl_scale)#90
                red_hu,red_su,red_vu = 179,255,255
                blue_sl_scale = 50/60.0
                blue_vl_scale = 50/60.0
                blue_hu_scale = 20/60.0
                blue_sl = 155 + int((two_led_length - 20)*blue_sl_scale)#155
                blue_vl = 110 + int((two_led_length - 20)*blue_vl_scale)#110
                blue_hu = 153 - int((two_led_length - 20)*blue_hu_scale)
                blue_hl,blue_su,blue_vu = 100,255,255
            elif two_led_length >= 80:
                red_hl,red_sl,red_vl = 150,140,120
                red_hu,red_su,red_vu = 179,255,255
                blue_hl,blue_sl,blue_vl = 100,190,160
                blue_hu,blue_su,blue_vu = 130,255,255
            else:
                red_hl,red_sl,red_vl = 135,70,80 #sl 135 80
                red_hu,red_su,red_vu = 179,255,255
                blue_hl,blue_sl,blue_vl = 100,135,90
                blue_hu,blue_su,blue_vu = 155,255,255
#---------------------------Get_Angle---------------------------
            two_led_angle,led_to_imgcenter_angle = Angle(new_list[0][0],new_list[1][0],new_list[0][1],new_list[1][1],two_point_center_x,two_point_center_y)
            modulated_Two_Led_Angle = Modulated_Two_Led_Angle(red_y,two_point_center_y,two_led_angle)
            modulated_Led_To_Imgcenter_Angle = Modulated_Led_To_Imgcenter_Angle(two_point_center_y,led_to_imgcenter_angle)
            print("Distance：" , distance , "    " , "Two LED length：" , two_led_length)
#---------------------------Control_Tello---------------------------
            if two_led_length >= 60 and two_led_length <= 75:
                if distance >= 45:
                    pid.update(distance)
                    speed = pid.output
                    roll,pitch,yaw = RC(modulated_Two_Led_Angle,modulated_Led_To_Imgcenter_Angle,speed)
                    Control_Tello("rc " + str(roll) + " " +str(pitch) + " " + str(0) + " " + str(yaw))
                else:
                    if two_led_length > 70:
                        Control_Tello("rc 0 0 0 0")
                        Control_Tello("land")
                        print(data_list)
                        cap.release()
                        sock.close()
                        cv2.destroyAllWindows()
                        break
                    else:
                        Control_Tello("rc 0 0 -20 0")
            elif two_led_length >= 75:
                if distance >= 100:
                    pid.update(distance)
                    speed = pid.output
                    roll,pitch,yaw = RC(modulated_Two_Led_Angle,modulated_Led_To_Imgcenter_Angle,speed)
                    Control_Tello("rc " + str(roll) + " " +str(pitch) + " " + str(0) + " " + str(yaw))
                else:
                    Control_Tello("rc 0 0 0 0")
                    Control_Tello("land")
                    print(data_list)
                    cap.release()
                    sock.close()
                    cv2.destroyAllWindows()
                    break
            else:
                if distance >= 55:
                    pid.update(distance)
                    speed = pid.output
                    roll,pitch,yaw = RC(modulated_Two_Led_Angle,modulated_Led_To_Imgcenter_Angle,speed)
                    Control_Tello("rc " + str(roll) + " " +str(pitch) + " " + str(0) + " " + str(yaw))
                else:
                    Control_Tello("rc 0 0 -30 0")
        except:
            red_hl,red_sl,red_vl = 135,60,80 #sl 135
            red_hu,red_su,red_vu = 179,255,255
            blue_hl,blue_sl,blue_vl = 100,135,90
            blue_hu,blue_su,blue_vu = 155,255,255
            if up < 2:
                if up_timer >= 2:
                    Control_Tello("rc 0 0 20 0")
                    up_timer = 0
                    up += 1
                else:
                    up_timer += time.perf_counter() - up_time
            else:
                if stop_timer >= 3:
                    Control_Tello("rc 0 0 0 0")
                    stop_timer = 0
                else:
                    stop_timer += time.perf_counter() - stop_time
            print('Can not see Tello',int(up_timer),int(stop_timer))
        print('-------------------------------------------')
        cv2.imshow("Led_Image", frame)
    except KeyboardInterrupt as e:
        Control_Tello("land")
        print(data_list)
        cap.release()
        sock.close()
        cv2.destroyAllWindows()
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        Control_Tello("land")
        print(data_list)
        cap.release()
        sock.close()
        cv2.destroyAllWindows()
        break
