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
        self.faceArr = [face(i, self.cubeArr) for i in range(6)]
        #self.topFace = face(0,self.cubeArr)
        #self.leftFace = face(1,self.cubeArr)

        return None


    def populateCube(self):

        for currFace in range(6):
            self.cubeArr.append([[currFace]*3 for i in range(3)])

        
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

        if clockwise:
            self.cubeArr[0] = self.cubeArr[1]
            self.cubeArr[1] = self.cubeArr[5]
            self.cubeArr[5] = self.cubeArr[3]
            self.cubeArr[3] = temp

        else:
            self.cubeArr[0] = self.cubeArr[3]
            self.cubeArr[3] = self.cubeArr[5]
            self.cubeArr[5] = self.cubeArr[1]
            self.cubeArr[1] = temp

    

    def turnCubeZ(self, clockwise = True):
        temp = self.cubeArr[1]

        if clockwise:
            self.cubeArr[1] = self.cubeArr[2]
            self.cubeArr[2] = self.cubeArr[3]
            self.cubeArr[3] = self.cubeArr[4]
            self.cubeArr[4] = temp

        else:
            self.cubeArr[1] = self.cubeArr[4]
            self.cubeArr[4] = self.cubeArr[3]
            self.cubeArr[3] = self.cubeArr[2]
            self.cubeArr[2] = temp

    

    def turnCubeY(self, clockwise = True):
        temp = self.cubeArr[0]

        if clockwise:
            self.cubeArr[0] = self.cubeArr[2]
            self.cubeArr[2] = self.cubeArr[5]
            self.cubeArr[5] = self.cubeArr[4]
            self.cubeArr[4] = temp

        else:
            self.cubeArr[0] = self.cubeArr[4]
            self.cubeArr[4] = self.cubeArr[5]
            self.cubeArr[5] = self.cubeArr[2]
            self.cubeArr[2] = temp



newCube = cube()
newCube.printCube()
run = True
while run:
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
    newCube.printCube()


#print(newCube.cubeArr)
#newCube.printCube()
#newCube.turnCubeZ(False)
#newCube.faceArr[1].rotateFace()
#newCube.printCube()
#print(a)
#newCube.rotateFace(a,False)
#print(a)
#a.reverse()
#print(a)
#newCube.rotate(newCube.topFace)
#print(newCube.cubeArr)
# CUBE INDEXING