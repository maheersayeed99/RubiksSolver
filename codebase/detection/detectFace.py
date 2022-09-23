import cv2
from detectionDatabases import *

class detectFace():

    def __init__(self,index) -> None:

        self.colorArr = [["k","k","k"],
                        ["k","k","k"],
                        ["k","k","k"]]
        self.index = index
        self.faceColor = indexArr[index]
        self.colorArr[1][1] = indexArr[index]
        
        pass

    def detectCenter(self):
        pass

    def resetFacet(self,row,col):
        if row == 1 and col == 1:
            self.colorArr[row][col] =   self.faceColor  
        else:
            self.colorArr[row][col] = "k"
        


    def populateArray(self, contours, color, coordinateArr):

        for row in range(len(self.colorArr)):               # iterates through every cell of the face
            for col in range(len(self.colorArr[0])):
                
                #self.resetFacet(row,col)
                for contour in contours:                    # Checks all the contours of the provided color
                    if cv2.pointPolygonTest(contour, coordinateArr[row][col], False) == 1:
                        self.colorArr[row][col] = color
                        
                
                
                

        
        return self.colorArr.copy()
                        



