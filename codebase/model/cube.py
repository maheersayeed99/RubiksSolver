from face import *
from part import *
import random

colorMap = {
        0 : "w",
        1 : "g", 
        2 : "r", 
        3 : "b", 
        4 : "o", 
        5 : "y"
        }

rotMap = {
        "U": (0,True),
        "I": (0,False),
        "L": (1,True),
        "P": (1,False),
        "F": (2,True),
        "G": (2,False),
        "R": (3,True),
        "T": (3,False),
        "B": (4,True),
        "N": (4,False),
        "D": (5,True),
        "S": (5,False)
        }

class cube:
    def __init__(self) -> None:
        
        self.cubeArr = []
        self.populateCube()
        self.faceArr = [face(i) for i in range(6)]
        self.edgeList = []
        self.cornerList = []
        
        return None


    def populatePieces(self):

        self.edgeList.append(edge(0, (2,0,1),(0,2,1)))
        self.edgeList.append(edge(1, (2,1,2),(3,1,0)))
        self.edgeList.append(edge(2, (2,2,1),(5,0,1)))
        self.edgeList.append(edge(3, (2,1,0),(1,1,2)))

        self.edgeList.append(edge(4, (1,0,1),(0,1,0)))
        self.edgeList.append(edge(5, (0,1,2),(3,0,1)))
        self.edgeList.append(edge(6, (3,2,1),(5,1,2)))
        self.edgeList.append(edge(7, (5,1,0),(1,2,1)))

        self.edgeList.append(edge(8, (4,0,1),(0,0,1)))
        self.edgeList.append(edge(9, (4,1,2),(1,1,0)))
        self.edgeList.append(edge(10, (4,2,1),(5,2,1)))
        self.edgeList.append(edge(11, (4,1,0),(3,1,2)))

        self.cornerList.apend(corner(0, (2,0,0),(1,0,2),(0,2,0)))
        self.cornerList.apend(corner(1, (2,0,2),(0,2,2),(3,0,0)))
        self.cornerList.apend(corner(2, (2,2,2),(3,2,0),(5,0,2)))
        self.cornerList.apend(corner(3, (2,2,0),(5,0,0),(1,2,2)))

        self.cornerList.apend(corner(4, (4,0,0),(3,0,2),(0,0,2)))
        self.cornerList.apend(corner(5, (4,0,2),(0,0,0),(1,0,0)))
        self.cornerList.apend(corner(6, (4,2,2),(1,2,0),(5,2,0)))
        self.cornerList.apend(corner(7, (4,2,0),(5,2,2),(3,2,2)))

    def populateCube(self):

        for currFace in range(6):
            self.cubeArr.append([[colorMap[currFace]]* 3 for i in range(3)])
    
    def resetCube(self):
        for currFace in range(6):
            self.cubeArr[currFace] = [[colorMap[currFace]]*3 for i in range(3)]

        
    def printCubeInt(self):
        
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


    def printCube(self):
        
        for i in range(len(self.cubeArr[0])):
            tempStr = " "
            print("     ",tempStr.join(self.cubeArr[0][i]))

        
        for i in range(len(self.cubeArr[1])):
            tempStr = " "
            tempStr = tempStr.join(self.cubeArr[1][i])+ " " + tempStr.join(self.cubeArr[2][i])+ " " + tempStr.join(self.cubeArr[3][i])+ " " + tempStr.join(self.cubeArr[4][i])
            print(tempStr)

        
        for i in range(len(self.cubeArr[5])):
            tempStr = " "
            print("     ",tempStr.join(self.cubeArr[5][i]))
            

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

    def singleMove(self,s):
        if s not in rotMap:
            print("INVALID")
            return
        targetFace, clockwise = rotMap[s]
        self.faceArr[targetFace].rotate(self.cubeArr, clockwise)

    def multipleMoves(self,s):
        for letter in s:
            self.singleMove(letter)
    
    def scramble(self, numMoves):
        for move in range(numMoves):
            key, val = random.choice(list(rotMap.items()))
            self.singleMove(key)



newCube = cube()
newCube.printCube()
newCube.scramble(20)
newCube.printCube()


'''
run = True
while run:
    print(newCube.cubeArr[0])
    #print(newCube.faceArr[0].currFace)
    print(newCube.faceArr[0].index)
    #print(newCube.faceArr[3].neighbors)
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

    elif val == "T":
        newCube.faceArr[0].rotate(newCube.cubeArr)
    elif val == "L":
        newCube.faceArr[1].rotate(newCube.cubeArr)
    elif val == "F":
        newCube.faceArr[2].rotate(newCube.cubeArr)
    elif val == "R":
        newCube.faceArr[3].rotate(newCube.cubeArr)
    elif val == "B":
        newCube.faceArr[4].rotate(newCube.cubeArr)
    elif val == "D":
        newCube.faceArr[5].rotate(newCube.cubeArr)
    
    elif val == "TP":
        newCube.faceArr[0].rotate(newCube.cubeArr, False)
    elif val == "LP":
        newCube.faceArr[1].rotate(newCube.cubeArr, False)
    elif val == "FP":
        newCube.faceArr[2].rotate(newCube.cubeArr, False)
    elif val == "RP":
        newCube.faceArr[3].rotate(newCube.cubeArr, False)
    elif val == "BP":
        newCube.faceArr[4].rotate(newCube.cubeArr, False)
    elif val == "DP":
        newCube.faceArr[5].rotate(newCube.cubeArr, False)

    
    elif val == "Reset":
        newCube.resetCube()

    else:
        print("invalid")
    newCube.printCube()
'''