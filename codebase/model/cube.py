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
            self.cubeArr.append([[currFace*(i+1)]*3 for i in range(3)])

    
    

newCube = cube()

print(newCube.cubeArr)
newCube.faceArr[1].rotateFace()
print(newCube.cubeArr)

#print(a)
#newCube.rotateFace(a,False)
#print(a)
#a.reverse()
#print(a)
#newCube.rotate(newCube.topFace)
#print(newCube.cubeArr)
# CUBE INDEXING