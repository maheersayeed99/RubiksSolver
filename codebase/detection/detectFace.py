import cv2
from detectionDatabases import *
from sklearn.cluster import KMeans


class detectFace():

    def __init__(self,index) -> None:

        self.colorArr = [["k","k","k"],         # Initially entire face is set to black
                        ["k","k","k"],
                        ["k","k","k"]]


        self.bgrArr = [[None,None,None],         # Initially entire face is set to black
                        [None,None,None],
                        [None,None,None]]

        self.index = index
        self.faceColor = indexArr[index]        
        self.colorArr[1][1] = indexArr[index]       # Center cell is made the color of the face, this eill not change
        
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

        self.colorArr[1][1] = self.faceColor            # recolors center piece to the face color
        return self.colorArr.copy()
                        
    
    def findDominantColor(self, coordinateArr, image):

        offset = 30
        rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        for row in range(len(self.colorArr)):               # iterates through every cell of the face
            for col in range(len(self.colorArr[0])):
                currY = coordinateArr[row][col][0]
                currX = coordinateArr[row][col][1]
                
                
                cropped = rgb[(currX-offset):(currX+offset), (currY-offset):(currY+offset)]
                #cv2.imshow("test", cropped)
                cropped = cropped.reshape(cropped.shape[0]*cropped.shape[1], 3)
                
                clf = KMeans(n_clusters= 1)
                clf.fit_predict(cropped)
                center_colors = clf.cluster_centers_
                self.bgrArr[row][col] = center_colors[0]

                print("heck: ", center_colors[0])    

        
        pass



