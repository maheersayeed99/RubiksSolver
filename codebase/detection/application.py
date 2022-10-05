import cv2
import numpy as np
from line import *
from detectFace import *
from detectionDatabases import *
import time



class app:
    def __init__(self, cube) -> None:
        
        # Cube taken from cube class
        self.cube = cube
        self.term = False
        
        # Draw dimensions and ares
        self.winWidth = 720
        self.winRealHeight = int((1080/1920)*self.winWidth)
        self.winHeight = self.winRealHeight-100
        self.boundSize = int(self.winHeight*0.75)
        self.topLeftx = 0
        self.topLefty = 0
        self.bottomRightx = 0
        self.bottomRighty = 0
        self.maskOffset = 20
        self.orientationOffset = 50
        self.regionArea = (self.boundSize- (2*self.maskOffset))**2

        # Initialize webcam video 
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,self.winWidth)
        self.cap.set(4,self.winRealHeight)

        

        # All canvases
        self.originalImage = None
        self.displayImage = None
        self.hsv = None
        self.dilation = None
        self.contours = None
        self.dilation = None

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
        self.hsvGroup = [nighttimeHSV, daytimeHSV]
        self.hsvArray = self.hsvGroup[0]
        

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


        # AUTO DETECT
        self.checking = False
        self.showing = False
        self.refTime = 0
        self.detectTolerance = 0.95
        self.solveTime = 3 #second
        self.showTime = self.solveTime + 2

        self.currMask = 2
        self.cannyParam1 = 116
        self.cannyParam2 = 203



    def populateLines(self):                    # Generates the 4 orientation lines

        middleX = self.winWidth//2
        middleY = self.winHeight//2
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
        

    def populateFaces(self):                        # Generates the 6 detection faces
        for i in range(6):
            self.faceList.append(detectFace(i))


    def changeMode(self, left = True):                      # Changes which face is active
        if left:
            self.faceList.append(self.faceList.pop(0))
        else:
            self.faceList.insert(0, self.faceList.pop())

        colorChange = orientationLineChanges[self.faceList[0].index]                # Change orientation line colors

        for index in range(len(self.orientationLines)):
            self.orientationLines[index].changeColor(bgrMap[colorChange[index]])


    def populateCube(self):                 # Generate result cube which will be populated with detected colors
        for i in range(6):
            self.cubeArr.append([["k","k","k"], ["k","k","k"], ["k","k","k"]])



    
    def generateColorMasks(self):               # Create 6 color masks with threshold data from databases.py

        
        whiteLower = np.array(self.hsvArray[0][0])
        whiteUpper = np.array(self.hsvArray[0][1])
        self.maskArr[0] = cv2.inRange(self.hsv,whiteLower,whiteUpper)
        self.colorMask = self.maskArr[0]

        greenLower = np.array(self.hsvArray[1][0])
        greenUpper = np.array(self.hsvArray[1][1])
        self.maskArr[1] = cv2.inRange(self.hsv,greenLower,greenUpper)
        self.colorMask += self.maskArr[1]

        '''redLower = np.array(self.hsvArray[2][0])
        redUpper = np.array(self.hsvArray[2][1])
        self.maskArr[2] = cv2.inRange(self.hsv,redLower,redUpper)
        self.colorMask += self.maskArr[2]'''

        redLower = np.array((0,50,50))
        redUpper = np.array((10,255,255))
        temp1 = cv2.inRange(self.hsv,redLower,redUpper)
        redLower = np.array((170,50,50))
        redUpper = np.array((180,255,255))
        temp2 = cv2.inRange(self.hsv,redLower,redUpper)
        self.maskArr[2] = temp1+temp2#q-self.maskArr[4]
        self.colorMask += self.maskArr[2]

        blueLower = np.array(self.hsvArray[3][0])
        blueUpper = np.array(self.hsvArray[3][1])
        self.maskArr[3] = cv2.inRange(self.hsv,blueLower,blueUpper)
        self.colorMask += self.maskArr[3]

        orangeLower = np.array(self.hsvArray[4][0])
        orangeUpper = np.array(self.hsvArray[4][1])
        self.maskArr[4] = cv2.inRange(self.hsv,orangeLower,orangeUpper)
        self.colorMask += self.maskArr[4]

        
        yellowLower = np.array(self.hsvArray[5][0])
        yellowUpper = np.array(self.hsvArray[5][1])
        self.maskArr[5] = cv2.inRange(self.hsv,yellowLower,yellowUpper)
        self.colorMask += self.maskArr[5]

        '''yellowLower = np.array((self.cannyParam1,50,0))
        yellowUpper = np.array((self.cannyParam2,255,255))
        self.maskArr[1] = cv2.inRange(self.hsv,yellowLower,yellowUpper)
        self.colorMask += self.maskArr[5]'''
        
        self.maskArr[0] = self.colorMask


    def getContours(self, dilated):                 # Get all contours in a given mask
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        filteredContours = []
        for currContour in contours:
            area = cv2.contourArea(currContour)
            if area > 0 and area < 145800:
                filteredContours.append(currContour)
        return filteredContours

    
    def drawContours(self, contours, canvas):               # Draw contours on the screen
        for currContour in contours:
            area = cv2.contourArea(currContour)
            if area > 0:
                thickness = int((1.5*area/self.regionArea)*5)
                cv2.drawContours(canvas, currContour, -1, (208,224,64), thickness)      # Turquoise
                #perimeter = cv2.arcLength(currContour, True)
                #approximate  = cv2.approxPolyDP(currContour,0.02*perimeter, True)
                #x, y, w, h = cv2.boundingRect(approximate)
                #cv2.rectangle(canvas, (x,y),(x+w,y+h), (255,255,255), 2)

    
    def generateCoordinates(self):          # Create a 2d array of coordinates that marks the center of each orientation square

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



    def drawFace(self, canvas):                         # Draw colored circles at the coordinate points based on the colors in the active face
        cubeFace = self.faceList[0].colorArr
        for row in range(len(cubeFace)):
            for col in range(len(cubeFace[0])):
                cv2.circle(canvas, self.coordinates[row][col], 10 , bgrMap[cubeFace[row][col]], -1)

    
    def getTotalArea(self):                             # This is used during auto detection of face color
        if len(self.contours) == 0:
            return 0
        else:
            return cv2.contourArea(self.contours[0])
        #for contour in self.contours:
        #    rslt+=cv2.contourArea(contour)
        return rslt


    def checkForCube(self):         # Function that checks if a cube is on screen, and runs detect color function if it is on screen longer than 3 seconds

        #print(self.getTotalArea()," ",self.regionArea)

        if self.getTotalArea() > (self.detectTolerance * self.regionArea) and self.checking == False and self.showing == False:
            self.refTime = time.time()
            self.checking = True
        
        elif self.showing == True:
            currTime = time.time() - self.refTime
            if currTime > self.showTime:
                self.changeMode()
                self.showing = False

        elif self.getTotalArea() > self.detectTolerance * self.regionArea:
            currTime = time.time() - self.refTime
            if currTime > self.solveTime:
                self.detectColors()
                self.checking = False
                self.showing = True
                        
        else:
            self.checking = False



    def detectColors(self):                             # MAIN FUNCTION, This uses the color masks to check the color of each detections square

        self.generateColorMasks()
        for index in range(len(self.maskArr)):
            kernel = np.ones((5,5))
            dilation = cv2.dilate(self.maskArr[index],kernel,iterations=1)
            contours = self.getContours(dilation)
            self.faceList[0].populateArray(contours, indexArr[index], self.coordinates)

        print(self.faceList[0].colorArr)
        self.cubeArr[self.faceList[0].index] = self.faceList[0].colorArr


    def generateSolution(self):                                     # Once self.cubeArr is copmpletely populated, this function solves the cube and prints the solition to the terminal
        self.cube.manualScramble(self.cube.cubeArr, self.cubeArr)
        self.cube.solveCube()


    def drawSolution(self):

        
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.6
        color = (250, 250, 250)
        thickness = 2

        lines = []
        maxLen = len(self.cube.screenString)
        increment = 62
        start = 0
        end = increment
        while maxLen>increment:
            lines.append(self.cube.screenString[start:end])
            start += increment
            end += increment
            maxLen -= increment
        lines.append(self.cube.screenString[start:])
        
        locIncrement = 0
        for line in lines:
            location = (30, self.winHeight + locIncrement)
            self.displayImage = cv2.putText(self.displayImage, line , location , font, fontScale, color, thickness, cv2.LINE_AA, False)
            locIncrement += 25


    # FUNCTIONS THAT RUN THE ENTIRE TIME

    def process(self):          # This function is mainly used to check whether a cube is on screen

        # Capture from webcam
        success, self.originalImage = self.cap.read()               

        # Resize image to webcam size
        self.originalImage = cv2.resize(self.originalImage, (self.winWidth, self.winRealHeight), interpolation= cv2.INTER_AREA)

        # Create mask that only fits square in the middle of the screen
        tempMask = np.zeros(self.originalImage.shape[:2], dtype="uint8")
        cv2.rectangle(tempMask, (self.topLeftx + self.maskOffset, self.topLefty+self.maskOffset), (self.bottomRightx -self.maskOffset, self.bottomRighty-self.maskOffset), 255, -1)
        
        # Make new image that is only the square of the original image
        squareImage = cv2.bitwise_and(self.originalImage,self.originalImage, mask = tempMask)
        
        # Potentially blur the image
        blurred = cv2.GaussianBlur(squareImage, (7,7), 1)

        # Potentially gray image
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

        # Potentially Canny
        canny = cv2.Canny(gray, self.cannyParam1, self.cannyParam2)

        
        # Change image to rgb image
        rgb = cv2.cvtColor(blurred,cv2.COLOR_BGR2RGB)

        # Change image to hsv image
        self.hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

        # Create masks for all 6 colors
        self.generateColorMasks()
        
        # Find contours of a single color
        kernel = np.ones((5,5))
        #dilation = cv2.dilate(self.maskArr[self.currMask],kernel,iterations=1)
        #dilation = cv2.dilate(self.colorMask,kernel,iterations=1)
        self.dilation = cv2.dilate(canny,kernel,iterations=2)
        self.contours = self.getContours(self.dilation)

        # Choose the image to display as the original image
        self.displayImage = self.originalImage.copy() # choose which version to display

        self.checkForCube()         

    
    
    def draw(self):     # Main draw function

        # Draw the 4 orientation lines on the screen
        for line in self.orientationLines:
            line.draw(self.displayImage)

        # Draw the face dots on the screen
        self.drawFace(self.displayImage)
        
        # Draw the single set of contours obtained from process (This is for debugging the color ranges)
        self.drawContours(self.contours, self.displayImage)

        # Mirror the image
        self.displayImage = cv2.flip(self.displayImage,1)

        self.drawSolution()
        
        # Display the image in one window
        #whiteCanvas = np.zeros([100,self.winWidth])
        #newImage = cv2.bitwise_and(whiteCanvas, self.displayImage)
        #self.displayImage = newImage
        
        #newImage = cv2.vconcat([self.displayImage, whiteCanvas])
        
        cv2.imshow(self.camWindow, self.displayImage)
        
        
        
        # Create a masked view of just one color and display it on a second window
        #masked = cv2.bitwise_and(self.displayImage, self.displayImage, mask = cv2.flip(self.maskArr[1],1))
        #masked = cv2.bitwise_and(self.displayImage, self.displayImage, mask = cv2.flip(self.colorMask,1))
        #cv2.imshow("Test", masked)
        #cv2.imshow("Test", self.dilation)

        #masked2 = cv2.bitwise_and(self.displayImage, self.displayImage, mask = cv2.flip(self.maskArr[5],1))
        #cv2.imshow("Test2", masked2)
        #cv2.imshow("Test", self.dilation)
        

    def run(self):          # User Input

        key = cv2.waitKey(1)

        if key == ord('q'):         # End
            self.term = True
        elif key == ord('r'):       # Next Face
            self.changeMode()
            print(self.faceList[0].index)
        elif key == ord('l'):       # Previous Face
            self.changeMode(False)
            print(self.faceList[0].index)
        elif key == ord('s'):       # Detect Colors
            self.detectColors()
        elif key == ord('z'):       # Lower Sensitivity 1
            self.cannyParam1-=1
            print(self.cannyParam1, " ", self.cannyParam2)
        elif key == ord('x'):       # Increase Sensitivity 1
            self.cannyParam1+=1
            print(self.cannyParam1, " ", self.cannyParam2)

        elif key == ord('v'):       # Increase Sensitivity 2
            self.cannyParam2+=1
            print(self.cannyParam1, " ", self.cannyParam2)
        elif key == ord('c'):       # Lower Sensitivity 2
            self.cannyParam2-=1
            print(self.cannyParam1, " ", self.cannyParam2)
        elif key == ord('m'):       # Solve (Only if all faces are occupied!)
            self.generateSolution()

        elif key == ord('n'):       # Change Threshold Group
            self.hsvGroup.append(self.hsvGroup.pop())
            self.hsvArray = self.hsvGroup[0]
            

    def terminate(self) -> bool:        # End application
        return self.term
