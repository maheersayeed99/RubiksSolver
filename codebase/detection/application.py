import cv2
import numpy as np


class app:
    def __init__(self) -> None:
        
        self.term = False
        
        self.winWidth = 720
        self.winHeight = int((1080/1920)*self.winWidth)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,self.winWidth)
        self.cap.set(4,self.winHeight)


        self.originalImage = None
        self.displayImage = None
        self.hsv = None
        self.dilation = None
        self.contours = None


        self.cannyParam1 = 100
        self.cannyParam2 = 0
        self.camWindow = "Camera"
        
        self.colorMask = None


        return


    def generateColorMasks(self):
        redLower = np.array([160,100,20])
        redUpper = np.array([179,255,255])
        mask1 = cv2.inRange(self.hsv,redLower,redUpper)

        orangeLower = np.array([ 4,100,100])
        orangeUpper = np.array([8,255,255])
        mask2 = cv2.inRange(self.hsv,orangeLower,orangeUpper)

        yellowLower = np.array([15,0,0])
        yellowUpper = np.array([36,255,255])
        mask3 = cv2.inRange(self.hsv,yellowLower,yellowUpper)

        greenLower = np.array([36,0,0])
        greenUpper = np.array([86,255,255])
        mask4 = cv2.inRange(self.hsv,greenLower,greenUpper)

        #blueLower = np.array([self.cannyParam1,0,0])
        #blueUpper = np.array([self.cannyParam2,255,255])
        #mask5 = cv2.inRange(self.hsv,blueLower,blueUpper)

        blueLower = np.array([110,62,62])
        blueUpper = np.array([130,255,255])
        mask5 = cv2.inRange(self.hsv,blueLower,blueUpper)

        
        
        self.colorMask = mask5


    def getContours(self, dilated):
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

    
    def drawContours(self, contours, original):
        for currContour in contours:
            area = cv2.contourArea(currContour)
            if area > 1000:
                cv2.drawContours(original, currContour, -1, (255,0,255), 2)
                perimeter = cv2.arcLength(currContour, True)
                approximate  = cv2.approxPolyDP(currContour,0.02*perimeter, True)
                x, y, w, h = cv2.boundingRect(approximate)
                cv2.rectangle(original, (x,y),(x+w,y+h), (255,255,255), 2)

    
            
    
    def process(self):
        success, self.originalImage = self.cap.read()

        self.originalImage = cv2.flip(self.originalImage,1)

        # original image
        self.originalImage = cv2.resize(self.originalImage, (self.winWidth, self.winHeight), interpolation= cv2.INTER_AREA)

        # blurred image
        blurred = cv2.GaussianBlur(self.originalImage, (7,7), 1)


        # rgb image

        rgb = cv2.cvtColor(blurred,cv2.COLOR_BGR2RGB)

        # hsv image

        self.hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        self.generateColorMasks()

        kernel = np.ones((5,5))
        dilation = cv2.dilate(self.colorMask,kernel,iterations=1)
        self.contours = self.getContours(dilation)


        self.displayImage = self.originalImage.copy() # choose which version to display

    def draw(self):

        self.drawContours(self.contours, self.colorMask)
        cv2.imshow(self.camWindow, self.colorMask)
        


    def run(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.term = True
        
        
        elif cv2.waitKey(1) & 0xFF == ord('e'):
            if self.cannyParam1 < 255:
                self.cannyParam1 += 1
        elif cv2.waitKey(1) & 0xFF == ord('w'):
            if self.cannyParam1 >5:
                self.cannyParam1 -= 1

        elif cv2.waitKey(1) & 0xFF == ord('d'):
            if self.cannyParam2 < 255:
                self.cannyParam2 += 1
        elif cv2.waitKey(1) & 0xFF == ord('s'):
            if self.cannyParam2 >0:
                self.cannyParam2 -= 1

        print("1: ",self.cannyParam1," 2: ",self.cannyParam2)
            

    def terminate(self) -> bool:
        return self.term



myApp = app()

while not myApp.terminate():
    myApp.process()
    myApp.run()
    myApp.draw()


