import cv2

class face():

    def __init__(self,index) -> None:

        self.colorArr = [["w","w","w"],
                        ["w","w","w"],
                        ["w","w","w"]]
        self.index = index
        
        pass


    def populateArray(self, contours, color, coordinateArr):

        for row in range(len(self.colorArr)):
            for col in range(len(self.colorArr[0])):
                for contour in contours:
                    if cv2.pointPolygonTest(contour, coordinateArr[row][col], False) == True:
                        self.colorArr[row][col] = color
        
        return self.colorArr.copy()
                        



