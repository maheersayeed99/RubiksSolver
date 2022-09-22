import cv2
import numpy as np
from line import *
from face import *
from databases import *



class app:
    def __init__(self) -> None:
        

        self.term = False
        
        self.winWidth = 720
        self.winHeight = int((1080/1920)*self.winWidth)
        self.boundSize = 0
        self.topLeftx = 0
        self.topLefty = 0

        self.orientationOffset = 50


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


        # ORIENTATION LINES
        self.orientationLines = []
        self.populateLines()


        # MODE
        self.faceList = []
        self.populateFaces()


        # CUBE
        self.cubeArr = []
        self.populateCube()

        # MASKS
        self.maskArr = [None]*5

        # COORDINATES
        self.coordinates = []
        self.generateCoordinates()
        print(self.coordinates)



        return


    def populateLines(self):

        middleX = self.winWidth//2
        middleY = self.winHeight//2
        self.boundSize = int(self.winHeight*0.8)
        halfBoundSize = self.boundSize//2
        self.topLeftx = middleX-halfBoundSize
        self.topLefty = middleY-halfBoundSize

        # Top Line
        self.orientationLines.append(line(middleX-halfBoundSize, middleY-halfBoundSize, self.boundSize, 0, 5))
        # Left Line
        self.orientationLines.append(line(middleX-halfBoundSize, middleY-halfBoundSize, 0, self.boundSize, 5))
        # Bottom Line
        self.orientationLines.append(line(middleX-halfBoundSize, middleY+halfBoundSize, self.boundSize, 0, 5))
        # Right Line
        self.orientationLines.append(line(middleX+halfBoundSize, middleY-halfBoundSize, 0, self.boundSize, 5))
        

    def populateFaces(self):
        for i in range(6):
            self.faceList.append(face(i))


    def changeMode(self, left = True):
        if left:
            self.faceList.append(self.faceList.pop(0))
        else:
            self.faceList.insert(0, self.faceList.pop())

        colorChange = orientationLineChanges[self.faceList[0].index]

        for index in range(len(self.orientationLines)):
            self.orientationLines[index].changeColor(colorMap[colorChange[index]])


    def populateCube(self):
        for i in range(6):
            self.cubeArr.append([["w","w","w"], ["w","w","w"], ["w","w","w"]])



    
    def generateColorMasks(self):
        redLower = np.array([160,100,20])
        redUpper = np.array([179,255,255])
        self.maskArr[0] = cv2.inRange(self.hsv,redLower,redUpper)

        orangeLower = np.array([ 4,100,100])
        orangeUpper = np.array([8,255,255])
        self.maskArr[1] = cv2.inRange(self.hsv,orangeLower,orangeUpper)

        yellowLower = np.array([15,0,0])
        yellowUpper = np.array([36,255,255])
        self.maskArr[2] = cv2.inRange(self.hsv,yellowLower,yellowUpper)

        greenLower = np.array([36,0,0])
        greenUpper = np.array([86,255,255])
        self.maskArr[3] = cv2.inRange(self.hsv,greenLower,greenUpper)

        blueLower = np.array([110,62,62])
        blueUpper = np.array([130,255,255])
        self.maskArr[4] = cv2.inRange(self.hsv,blueLower,blueUpper)



    def getContours(self, dilated):
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

    
    def drawContours(self, contours, original):
        for currContour in contours:
            area = cv2.contourArea(currContour)
            if area > 1000:
                cv2.drawContours(original, currContour, -1, (255,0,255), 2)
                #perimeter = cv2.arcLength(currContour, True)
                #approximate  = cv2.approxPolyDP(currContour,0.02*perimeter, True)
                #x, y, w, h = cv2.boundingRect(approximate)
                #cv2.rectangle(original, (x,y),(x+w,y+h), (255,255,255), 2)

    
    def generateCoordinates(self):

        for i in range(3):
            self.coordinates.append([[0,0,0],[0,0,0],[0,0,0]])

        squareSize = self.boundSize//3
        halfBoundSize = squareSize//2

        topLeftx = self.topLeftx-halfBoundSize
        topLefty = self.topLefty-halfBoundSize

        for row in range(1,4):
            for col in range(1,4):
                tempX = topLeftx + squareSize*col
                tempY = topLefty + squareSize*row
                self.coordinates[row-1][col-1] = (tempX,tempY)

    
    def detectColors(self):

        self.generateColorMasks()
        for index in range(len(self.maskArr)):
            kernel = np.ones((5,5))
            dilation = cv2.dilate(self.maskArr[index],kernel,iterations=1)
            contours = self.getContours(dilation)
            self.faceList[0].populateArray(contours, indexArr[index], self.coordinates)

        print(self.faceList[0].colorArr)
        self.cubeArr[self.faceList[0].index] = self.faceList[0].colorArr





    
            
    
    def process(self):
        success, self.originalImage = self.cap.read()

        #self.originalImage = cv2.flip(self.originalImage,1)

        # original image
        self.originalImage = cv2.resize(self.originalImage, (self.winWidth, self.winHeight), interpolation= cv2.INTER_AREA)

        # blurred image
        #blurred = cv2.GaussianBlur(self.originalImage, (7,7), 1)


        # rgb image

        rgb = cv2.cvtColor(self.originalImage,cv2.COLOR_BGR2RGB)

        # hsv image

        self.hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        #self.generateColorMasks()

        #kernel = np.ones((5,5))
        #dilation = cv2.dilate(self.colorMask,kernel,iterations=1)
        #self.contours = self.getContours(dilation)


        self.displayImage = self.originalImage.copy() # choose which version to display

    def draw(self):

        #self.drawContours(self.contours, self.displayImage)
        
        for line in self.orientationLines:
            line.draw(self.displayImage)
        
        cv2.imshow(self.camWindow, self.displayImage)
        


    def run(self):
        '''if cv2.waitKey(1) & 0xFF == ord('q'):
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
                self.cannyParam2 -= 1'''

        #print("1: ",self.cannyParam1," 2: ",self.cannyParam2)


        key = cv2.waitKey(1)
        if key == ord('q'):
            self.term = True
        elif key == ord('r'):
            self.changeMode()
            print(self.faceList[0].index)
        elif key == ord('l'):
            self.changeMode(False)
            print(self.faceList[0].index)
        elif key == ord('s'):
            self.detectColors()
        elif key == ord('t'):
            pass
        elif key == ord('c'):
            pass
        elif key == 27:
            pass
            

    def terminate(self) -> bool:
        return self.term



myApp = app()

while not myApp.terminate():
    myApp.process()
    myApp.run()
    myApp.draw()


