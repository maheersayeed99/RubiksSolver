from face import *
from part import *
import random
import copy

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

class facet:
    def __init__(self, color) -> None:
        self.color = color
        self.parent = None
        self.faces = [0]*6

    def isSame(self, other):
        return self.color == other.color and self.faces == other.faces


class cube:
    def __init__(self) -> None:
        
        self.cubeArr = []
        self.populateCube()
        self.faceArr = [face(i, self.cubeArr) for i in range(6)]
        self.startArr = copy.deepcopy(self.cubeArr)
        
        
        self.pieceList = []
        self.populatePieces()


        self.solveGraph = []
        return None

    def populatePieces(self):

        self.pieceList.append(edge(0, (2,0,1),(0,2,1)))
        self.pieceList.append(edge(1, (2,1,2),(3,1,0)))
        self.pieceList.append(edge(2, (2,2,1),(5,0,1)))
        self.pieceList.append(edge(3, (2,1,0),(1,1,2)))

        self.pieceList.append(edge(4, (1,0,1),(0,1,0)))
        self.pieceList.append(edge(5, (0,1,2),(3,0,1)))
        self.pieceList.append(edge(6, (3,2,1),(5,1,2)))
        self.pieceList.append(edge(7, (5,1,0),(1,2,1)))

        self.pieceList.append(edge(8, (4,0,1),(0,0,1)))
        self.pieceList.append(edge(9, (4,1,2),(1,1,0)))
        self.pieceList.append(edge(10, (4,2,1),(5,2,1)))
        self.pieceList.append(edge(11, (4,1,0),(3,1,2)))

        self.pieceList.append(corner(12, (2,0,0),(1,0,2),(0,2,0)))
        self.pieceList.append(corner(13, (2,0,2),(0,2,2),(3,0,0)))
        self.pieceList.append(corner(14, (2,2,2),(3,2,0),(5,0,2)))
        self.pieceList.append(corner(15, (2,2,0),(5,0,0),(1,2,2)))

        self.pieceList.append(corner(16, (4,0,0),(3,0,2),(0,0,2)))
        self.pieceList.append(corner(17, (4,0,2),(0,0,0),(1,0,0)))
        self.pieceList.append(corner(18, (4,2,2),(1,2,0),(5,2,0)))
        self.pieceList.append(corner(19, (4,2,0),(5,2,2),(3,2,2)))

    def populateCube(self):
        for i in  range(6):
            self.cubeArr.append([[None]* 3 for i in range(3)])

        for currFace in range(6):
            for row in range(3):
                for col in range(3):
                    tempFacet = facet(colorMap[currFace])
                    self.cubeArr[currFace][row][col] = tempFacet

            #self.cubeArr.append([[colorMap[currFace]]* 3 for i in range(3)])
        
    
    def resetCube(self):
        #for currFace in range(6):
        #    self.cubeArr[currFace] = [[colorMap[currFace]]*3 for i in range(3)]
        self.cubeArr = self.startArr
        self.startArr = copy.deepcopy(self.cubeArr)



        

    '''def printCube(self, cube):
        
        for i in range(len(cube[0])):
            tempStr = " "
            print("     ",tempStr.join(cube[0][i]))

        
        for i in range(len(cube[1])):
            tempStr = " "
            tempStr = tempStr.join(cube[1][i])+ " " + tempStr.join(cube[2][i])+ " " + tempStr.join(cube[3][i])+ " " + tempStr.join(cube[4][i])
            print(tempStr)

        
        for i in range(len(cube[5])):
            tempStr = " "
            print("     ",tempStr.join(cube[5][i]))
            

        print("\n")'''
    
    def printCube(self,cube):

        for i in range(len(cube[0])):
            print("     ",cube[0][i][0].color,cube[0][i][1].color,cube[0][i][2].color)

        for i in range(len(cube[1])):
            print(cube[1][i][0].color, cube[1][i][1].color, cube[1][i][2].color, \
                    cube[2][i][0].color,cube[2][i][1].color,cube[2][i][2].color, \
                    cube[3][i][0].color,cube[3][i][1].color,cube[3][i][2].color, \
                    cube[4][i][0].color,cube[4][i][1].color,cube[4][i][2].color)


        for i in range(len(cube[5])):
            print("     ",cube[5][i][0].color,cube[5][i][1].color,cube[5][i][2].color)



            

    def turnCubeX(self, clockwise = True):
        temp = self.cubeArr[0]
        tempStart = self.startArr[0]

        if clockwise == True:
            self.cubeArr[0], self.startArr[0] = self.cubeArr[1], self.startArr[1]
            self.cubeArr[1], self.startArr[1] = self.cubeArr[5], self.startArr[5]
            self.cubeArr[5], self.startArr[5] = self.cubeArr[3], self.startArr[3]
            self.cubeArr[3], self.startArr[3] = temp, tempStart

        else:
            self.cubeArr[0], self.startArr[0] = self.cubeArr[3], self.startArr[3]
            self.cubeArr[3], self.startArr[3] = self.cubeArr[5], self.startArr[5]
            self.cubeArr[5], self.startArr[5] = self.cubeArr[1], self.startArr[1]
            self.cubeArr[1], self.startArr[1] = temp, tempStart

        self.faceArr[0].rotateFace(self.cubeArr, clockwise)
        self.faceArr[1].rotateFace(self.cubeArr, clockwise)
        self.faceArr[2].rotateFace(self.cubeArr, clockwise)
        self.faceArr[3].rotateFace(self.cubeArr, clockwise)
        self.faceArr[4].rotateFace(self.cubeArr, not clockwise)
        self.faceArr[5].rotateFace(self.cubeArr, clockwise)
    

    def turnCubeZ(self, clockwise = True):
        temp = self.cubeArr[1]
        tempStart = self.startArr[1]

        if clockwise == True:
            self.cubeArr[1], self.startArr[1] = self.cubeArr[2], self.startArr[2]
            self.cubeArr[2], self.startArr[2] = self.cubeArr[3], self.startArr[3]
            self.cubeArr[3], self.startArr[3] = self.cubeArr[4], self.startArr[4]
            self.cubeArr[4], self.startArr[4] = temp, tempStart

        else:
            self.cubeArr[1], self.startArr[1] = self.cubeArr[4], self.startArr[4]
            self.cubeArr[4], self.startArr[4] = self.cubeArr[3], self.startArr[3]
            self.cubeArr[3], self.startArr[3] = self.cubeArr[2], self.startArr[2]
            self.cubeArr[2], self.startArr[2] = temp, tempStart

        self.faceArr[0].rotateFace(self.cubeArr, clockwise)
        self.faceArr[5].rotateFace(self.cubeArr, not clockwise)

    
    def turnCubeY(self, clockwise = True):
        
        temp = self.cubeArr[0]
        tempStart = self.startArr[0]

        if clockwise == True:
            self.cubeArr[0], self.startArr[0] = self.cubeArr[2], self.startArr[2]
            self.cubeArr[2], self.startArr[2] = self.cubeArr[5], self.startArr[5]
            self.cubeArr[5], self.startArr[5] = self.cubeArr[4], self.startArr[4]
            self.cubeArr[4], self.startArr[4] = temp, tempStart

        else:
            self.cubeArr[0], self.startArr[0] = self.cubeArr[4], self.startArr[4]
            self.cubeArr[4], self.startArr[4] = self.cubeArr[5], self.startArr[5]
            self.cubeArr[5], self.startArr[5] = self.cubeArr[2], self.startArr[2]
            self.cubeArr[2], self.startArr[2] = temp, tempStart

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


    ###################################    SOLVE   ####################################################

    # TODO
    # need to figure out node class for pathfinding
    # thinking lookup tables for each type of rotation, problem is the lookup tables could also be used for the regular rotation mechanism
    # Seems like hard-coding, not an elegant solution
    # maybe research other ways to rotate mathematically 



    # instead of string, make every cell a facelet
    # every facelet should be attached to a cubelet parent
    # iterate through every piece and check if it moves
    # if it moves find current piece from graph
    # find new piece location from graph
    # add edge to piece


    # find piece
    '''
    def findPiece(self, target, currCube):

        targetPiece = self.pieceList[target]
        
        for idx in range(len(self.pieceList)):
            if self.pieceList[idx].locate(targetPiece,currCube,self.startArr):
                return idx
        return None
    '''

    def findPiece(self, pos, cube1, cube2):
        for currFace in range(6):
            for row in range(3):
                for col in range(3):
                    if cube1[pos[0]][pos[1]][pos[2]].isSame(cube2[currFace][row][col]):
                        return (currFace, row, col)


    def generateGraph(self, moves):
        self.solveGraph = []

        for currFace in range(6):
            temp2 = []
            for row in range(3):
                temp1 = []
                for col in range(3):
                    temp1.append(node((currFace,row,col)))
                temp2.append(temp1)
            self.solveGraph.append(temp2)
        



    


    # Assign an object to every facelet and a parent
    # The parent will be used to tell facelets apart
    # After a rotation, the facelets at each cell move
    # but each facelet still points to the same parent pieces

    # Find facelet index in scrambled cube
    # Rotate (facelets will move)
    # check 

    # Make rotation follow the facelets
    # Initialize Graph
    # Check if
    


    # NEW POWERS
    # make list of nodes for every facet
    # every facet has a list of edges that move it to another facet based on a move
    # for pathfind,

class node:
    def __init__(self,pos) -> None:
        self.pos = pos
        self.parent = None
        self.changeList = []
        
class change:
    def __init__(self) -> None:
        self.parent = None
        self.change = ""
        self.targetPiece = None

newCube = cube()
newCube.scramble(20)
newCube.printCube(newCube.cubeArr)
newCube.printCube(newCube.startArr)
print(newCube.findPiece((2,1,2),newCube.startArr,newCube.cubeArr))
print(newCube.cubeArr[0][0][0])
print(newCube.cubeArr[0][0][1])

#newCube.faceArr[0].rotate(newCube.cubeArr)

#newCube.printCube(newCube.startArr)


#print(newCube.findPiece(2, newCube.cubeArr))


#newCube.scramble(20)
#newCube.printCube()


'''
run = True
while run:
    print(newCube.cubeArr[0])
    #print(newCube.faceArr[0].currFace)
    print(newCube.faceArr[0].index)
    #print(newCube.faceArr[3].neighbors)
    val = input("input: ")
    if val == "END":
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

    elif val == "SCRAMBLE":
        newCube.scramble(20)
    elif val == "RESET":
        newCube.resetCube()
    elif val == "TEST":
        if newCube.edgeList[0].isSame(newCube.cubeArr,newCube.startArr):
            print("They are the same")
        else:
            print("These are different")

    else:
        print("invalid")
    newCube.printCube(newCube.cubeArr)
    newCube.printCube(newCube.startArr)

'''