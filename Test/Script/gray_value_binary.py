import cv2
import numpy as np

image = cv2.imread(r'..\img\led5.png')
gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
blue1 , green1 , red1 = cv2.split(image)
c,r = gray.shape[:2]
w,h = int(r/20),int(c/20)
white = np.ones((h,w),np.uint8)*255
black = np.zeros((h,w),np.uint8)

for a in range(20):
    for b in range(20):
        imggray  = gray[h*a:h*(a+1),w*b:w*(b+1)]
        img = image[h*a:h*(a+1),w*b:w*(b+1)]
        blue,green,red = cv2.split(img)
        v = int(np.mean(imggray))
        vb,vg,vr = int(np.mean(blue)),int(np.mean(green)),int(np.mean(red))
        if vr-vg>50 and vr>v:
            img1 = white
        else:
            img1 = black
        if b==0:
            img2 = img1
        else:
            img2 = np.concatenate((img2,img1),axis =1)
    if a == 0:
        img3 = img2
    else:
        img3 = np.concatenate((img3,img2),axis=0)       

for c in range(20):
    for d in range(20):
        imggray  = gray[h*c:h*(c+1),w*d:w*(d+1)]
        img = image[h*c:h*(c+1),w*d:w*(d+1)]
        blue,green,red = cv2.split(img)
        v = int(np.mean(imggray))
        vb,vg,vr = int(np.mean(blue)),int(np.mean(green)),int(np.mean(red))  
        #print vr
        if vb-vr>50 and vb>v:
            imga = white
        else:
            imga = black
        if d == 0:
            imgb = imga
        else:
            imgb = np.concatenate((imgb,imga),axis =1)
    if c == 0:
        imgc = imgb
    else:
        imgc = np.concatenate((imgc,imgb),axis=0)
cv2.imshow("imgRinary" , img3)
cv2.waitKey(0)   
cv2.imshow("imgBBinary" , imgc)
cv2.waitKey(0)
cv2.destroyAllWindows()