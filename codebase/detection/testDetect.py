import cv2


winWidth = 720
winHeight = int((1080/1920)*winWidth)

capture = cv2.VideoCapture(0)


capture.set(3, winWidth)
capture.set(4,winHeight)


def getContours(img, inputContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for currContour in contours:
        area = cv2.contourArea(currContour)
        if area < 100000 and area > 10000:
            cv2.drawContours(inputContour, currContour, -1, (255,0,255), 7)
            perimeter = cv2.arcLength(currContour, True)
            approximate  = cv2.approxPolyDP(currContour,0.02*perimeter, True)
            #print(approximate)
            x, y, w, h = cv2.boundingRect(approximate)
            cv2.rectangle(inputContour, (x,y),(x+w,y+h), (255,255,255), 5)
            cv2.line(inputContour, (10,10),(470,10),(255,255,0),5 )

        


def nothing(a):
    
    return a

cv2.namedWindow("P")
cv2.resizeWindow("P", 480, 240)
cv2.createTrackbar("Threshold1", "P", 30, 255, nothing)
cv2.createTrackbar("Threshold2", "P", 30, 255, nothing)

import numpy as np

while True:
    success, img = capture.read()

    img = cv2.resize(img, (winWidth, winHeight), interpolation=cv2.INTER_AREA)

    inputContour = img.copy()

    blurred = cv2.GaussianBlur(img, (7,7), 1)
    #blurred = cv2.GaussianBlur(img, (7,7),1)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    threshold1 = int(cv2.getTrackbarPos("Threshold1", "P"))
    threshold2 = int(cv2.getTrackbarPos("Threshold2", "P"))

    canny = cv2.Canny(gray,threshold1,threshold2)

    kernel = np.ones((5,5))
    dilation = cv2.dilate(canny,kernel,iterations=1)

    getContours(dilation, inputContour)



    cv2.imshow("Window", inputContour)
    #cv2.imshow("Window", canny)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break