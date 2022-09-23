import cv2
import numpy as np
from line import *
from detectFace import *
from detectionDatabases import *



class app:
    def __init__(self, cube) -> None:
        
        self.cube = cube
        self.term = False
        
        self.winWidth = 720
        self.winHeight = int((1080/1920)*self.winWidth)
        self.boundSize = 0
        self.topLeftx = 0
        self.topLefty = 0
        self.bottomRightx = 0
        self.bottomRighty = 0

        self.orientationOffset = 50


        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,self.winWidth)
        self.cap.set(4,self.winHeight)


        self.originalImage = None
        self.displayImage = None
        self.hsv = None
        self.dilation = None
        self.contours = None


        self.cannyParam1 = 110
        self.cannyParam2 = 130
        self.camWindow = "Camera"
        

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
        self.maskArr = [None]*6
        self.colorMask = None
        self.currMask = 3

        # NOTES
        '''
        White is not working at all, seems to change drastically given the time of day
        Green is working perfectly
        Red is working decently could be better but totally acceptable
            Works great up close
        Blue is having a LOT of trouble, mixing in with white and sometimes not detecting itself
            Solution could be to darken it witha marker and also tinker with the hsl values
        Orange works surprisingly well but not crazy reliable, might just be a tuning issue
        Yellow works good but interesting phenonmenon with yellow/green where yellow encapsulates green but doesnt shade it, when this happens, the contour lines get confused
            Solution to this is very simple, make the bounding box slightly smaller that the axtual box
            Works well a little farther away
                
        '''

        # COORDINATES
        self.coordinates = []
        self.generateCoordinates()
        print(self.coordinates)



        return


    def populateLines(self):

        middleX = self.winWidth//2
        middleY = self.winHeight//2
        self.boundSize = int(self.winHeight*0.75)
        halfBoundSize = self.boundSize//2
        lineLength = int(self.boundSize//2 * 0.5)
        self.topLeftx = middleX-halfBoundSize
        self.topLefty = middleY-halfBoundSize
        self.bottomRightx = middleX+halfBoundSize
        self.bottomRighty = middleY+halfBoundSize


        # Top Line
        self.orientationLines.append(line(middleX-lineLength, middleY-halfBoundSize, lineLength*2 , 0, 5, bgrMap["o"]))
        # Left Line
        self.orientationLines.append(line(middleX-halfBoundSize, middleY-lineLength, 0, lineLength*2, 5, bgrMap["g"]))
        # Bottom Line
        self.orientationLines.append(line(middleX-lineLength, middleY+halfBoundSize, lineLength*2, 0, 5, bgrMap["r"]))
        # Right Line
        self.orientationLines.append(line(middleX+halfBoundSize, middleY-lineLength, 0, lineLength*2 , 5, bgrMap["b"]))
        

    def populateFaces(self):
        for i in range(6):
            self.faceList.append(detectFace(i))


    def changeMode(self, left = True):
        if left:
            self.faceList.append(self.faceList.pop(0))
        else:
            self.faceList.insert(0, self.faceList.pop())

        colorChange = orientationLineChanges[self.faceList[0].index]

        for index in range(len(self.orientationLines)):
            self.orientationLines[index].changeColor(bgrMap[colorChange[index]])


    def populateCube(self):
        for i in range(6):
            self.cubeArr.append([["k","k","k"], ["k","k","k"], ["k","k","k"]])



    
    def generateColorMasks(self):

        
        whiteLower = np.array([0,0,168])
        whiteUpper = np.array([172,111,255])
        self.maskArr[0] = cv2.inRange(self.hsv,whiteLower,whiteUpper)
        self.colorMask = self.maskArr[0]

        greenLower = np.array([36,0,0])
        greenUpper = np.array([86,255,255])
        self.maskArr[1] = cv2.inRange(self.hsv,greenLower,greenUpper)
        self.colorMask += self.maskArr[1]

        redLower = np.array([160,100,20])
        redUpper = np.array([179,255,255])
        self.maskArr[2] = cv2.inRange(self.hsv,redLower,redUpper)
        self.colorMask += self.maskArr[2]

        #blueLower = np.array([110,62,62])
        #blueUpper = np.array([130,255,255])
        blueLower = np.array([96,62,62])
        blueUpper = np.array([130,255,255])
        self.maskArr[3] = cv2.inRange(self.hsv,blueLower,blueUpper)
        self.colorMask += self.maskArr[3]

        orangeLower = np.array([ 4,100,100])
        orangeUpper = np.array([8,255,255])
        self.maskArr[4] = cv2.inRange(self.hsv,orangeLower,orangeUpper)
        self.colorMask += self.maskArr[4]

        yellowLower = np.array([15,0,0])
        yellowUpper = np.array([36,255,255])
        self.maskArr[5] = cv2.inRange(self.hsv,yellowLower,yellowUpper)
        self.colorMask += self.maskArr[5]

        self.maskArr[0] = self.colorMask


        
        

        



    def getContours(self, dilated):
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        filteredContours = []
        for currContour in contours:
            area = cv2.contourArea(currContour)
            if area > 1000 and area < 145800:
                filteredContours.append(currContour)
        return filteredContours

    
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



    def drawFace(self, canvas):
        cubeFace = self.faceList[0].colorArr
        for row in range(len(cubeFace)):
            for col in range(len(cubeFace[0])):
                cv2.circle(canvas, self.coordinates[row][col], 10 , bgrMap[cubeFace[row][col]], -1)

    
    def detectColors(self):

        self.generateColorMasks()
        for index in range(len(self.maskArr)):
            kernel = np.ones((5,5))
            dilation = cv2.dilate(self.maskArr[index],kernel,iterations=1)
            contours = self.getContours(dilation)
            self.faceList[0].populateArray(contours, indexArr[index], self.coordinates)

        print(self.faceList[0].colorArr)
        self.cubeArr[self.faceList[0].index] = self.faceList[0].colorArr


    def generateSolution(self):
        self.cube.manualScramble(self.cube.cubeArr, self.cubeArr)
        self.cube.solveCube()
        print(self.cube.solution)

    
    def process(self):

        # Capture from webcam
        success, self.originalImage = self.cap.read()               

        # Resize image to webcam size
        self.originalImage = cv2.resize(self.originalImage, (self.winWidth, self.winHeight), interpolation= cv2.INTER_AREA)

        # Create mask that only fits square in the middle of the screen
        tempMask = np.zeros(self.originalImage.shape[:2], dtype="uint8")
        cv2.rectangle(tempMask, (self.topLeftx + 20, self.topLefty+20), (self.bottomRightx -20, self.bottomRighty-20), 255, -1)
        
        # Make new image that is only the square of the original image
        squareImage = cv2.bitwise_and(self.originalImage,self.originalImage, mask = tempMask)
        
        # Potentially blur the image
        blurred = cv2.GaussianBlur(squareImage, (7,7), 1)

        


        # Change image to rgb image
        rgb = cv2.cvtColor(blurred,cv2.COLOR_BGR2RGB)

        # Change image to hsv image
        self.hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

        # Create masks for all 6 colors
        self.generateColorMasks()
        
        # Find contours of a single color
        kernel = np.ones((5,5))
        dilation = cv2.dilate(self.maskArr[self.currMask],kernel,iterations=1)
        #dilation = cv2.dilate(self.colorMask,kernel,iterations=1)
        self.contours = self.getContours(dilation)

        # Choose the image to display as the original image
        self.displayImage = self.originalImage.copy() # choose which version to display

    def draw(self):

        # Draw the 4 orientation lines on the screen
        for line in self.orientationLines:
            line.draw(self.displayImage)

        # Draw the face dots on the screen
        self.drawFace(self.displayImage)
        
        # Draw the single set of contours obtained from process (This is for debugging the color ranges)
        self.drawContours(self.contours, self.displayImage)

        # Mirror the image
        self.displayImage = cv2.flip(self.displayImage,1)
        
        # Display the image in one window
        cv2.imshow(self.camWindow, self.displayImage)
        
        # Create a masked view of just one color and display it on a second window
        masked = cv2.bitwise_and(self.displayImage, self.displayImage, mask = cv2.flip(self.maskArr[self.currMask],1))
        #masked = cv2.bitwise_and(self.displayImage, self.displayImage, mask = cv2.flip(self.colorMask,1))
        cv2.imshow("Test", masked)
        

    def run(self):

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
        elif key == ord('z'):
            self.cannyParam1-=1
            print(self.cannyParam1, " ", self.cannyParam2)
        elif key == ord('x'):
            self.cannyParam1+=1
            print(self.cannyParam1, " ", self.cannyParam2)

        elif key == ord('v'):
            self.cannyParam2+=1
            print(self.cannyParam1, " ", self.cannyParam2)
        elif key == ord('c'):
            self.cannyParam2-=1
            print(self.cannyParam1, " ", self.cannyParam2)
        elif key == ord('m'):
            self.generateSolution()
            

    def terminate(self) -> bool:
        return self.term






