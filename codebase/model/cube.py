from enum import Enum
from face import *
'''

CENTERS

      # # #
      # # #
      # # #
# # # # # # # # # # # #
# # # # # # # # # # # #
# # # # # # # # # # # #   
      # # #
      # # #
      # # #

'''
class color(Enum):
    white = 1
    green = 2
    red = 3
    blue = 4
    orange = 5
    yellow = 6

class facet:
    def __init__(self) -> None:
        return None

class cube:
    def __init__(self) -> None:

        self.cubeArr = []
        self.populateCube()
        self.faceArr = [face(i) for i in range(6)]
        
        return None


    def populateCube(self):

        for currFace in range(6):
            self.cubeArr.append([[currFace*i]*3 for i in range(3)])

        
    def printCube(self):
        
        for i in range(len(self.cubeArr[0])):
            print("         ",self.cubeArr[0][i])

        print("\n")

        for i in range(len(self.cubeArr[1])):
            print(self.cubeArr[1][i], self.cubeArr[2][i], self.cubeArr[3][i], self.cubeArr[4][i])

        print("\n")

        for i in range(len(self.cubeArr[5])):
            print("         ",self.cubeArr[5][i])

        print("\n")
        print("\n")
            


    
    def turnCubeX(self, clockwise = True):
        temp = self.cubeArr[0]

        if clockwise == True:
            self.cubeArr[0] = self.cubeArr[1]
            self.cubeArr[1] = self.cubeArr[5]
            self.cubeArr[5] = self.cubeArr[3]
            self.cubeArr[3] = temp

        else:
            self.cubeArr[0] = self.cubeArr[3]
            self.cubeArr[3] = self.cubeArr[5]
            self.cubeArr[5] = self.cubeArr[1]
            self.cubeArr[1] = temp

        self.faceArr[0].rotateFace(self.cubeArr, clockwise)
        self.faceArr[1].rotateFace(self.cubeArr, clockwise)
        self.faceArr[2].rotateFace(self.cubeArr, clockwise)
        self.faceArr[3].rotateFace(self.cubeArr, clockwise)
        self.faceArr[4].rotateFace(self.cubeArr, not clockwise)
        self.faceArr[5].rotateFace(self.cubeArr, clockwise)
    

    def turnCubeZ(self, clockwise = True):
        temp = self.cubeArr[1]

        if clockwise == True:
            self.cubeArr[1] = self.cubeArr[2]
            self.cubeArr[2] = self.cubeArr[3]
            self.cubeArr[3] = self.cubeArr[4]
            self.cubeArr[4] = temp

        else:
            self.cubeArr[1] = self.cubeArr[4]
            self.cubeArr[4] = self.cubeArr[3]
            self.cubeArr[3] = self.cubeArr[2]
            self.cubeArr[2] = temp

        self.faceArr[0].rotateFace(self.cubeArr, clockwise)
        self.faceArr[5].rotateFace(self.cubeArr, not clockwise)

    
    def turnCubeY(self, clockwise = True):
        
        temp = self.cubeArr[0]

        if clockwise == True:
            self.cubeArr[0] = self.cubeArr[2]
            self.cubeArr[2] = self.cubeArr[5]
            self.cubeArr[5] = self.cubeArr[4]
            self.cubeArr[4] = temp

        else:
            self.cubeArr[0] = self.cubeArr[4]
            self.cubeArr[4] = self.cubeArr[5]
            self.cubeArr[5] = self.cubeArr[2]
            self.cubeArr[2] = temp

        self.faceArr[1].rotateFace(self.cubeArr, not clockwise)
        self.faceArr[3].rotateFace(self.cubeArr, clockwise)
        self.faceArr[4].rotateFace(self.cubeArr)
        self.faceArr[4].rotateFace(self.cubeArr)
        self.faceArr[5].rotateFace(self.cubeArr)
        self.faceArr[5].rotateFace(self.cubeArr)


newCube = cube()
newCube.printCube()
run = True
while run:
    print(newCube.cubeArr[0])
    #print(newCube.faceArr[0].currFace)
    print(newCube.faceArr[0].index)
    val = input("input: ")
    if val == "end":
        run = False
    elif val == "X":
        newCube.turnCubeX()
    elif val == "RX":
        newCube.turnCubeX(False)
    elif val == "Y":
        newCube.turnCubeY()
    elif val == "RY":
        newCube.turnCubeY(False)
    elif val == "Z":
        newCube.turnCubeZ()
    elif val == "RZ":
        newCube.turnCubeZ(False)
    else:
        print("invalid")
    newCube.printCube()
