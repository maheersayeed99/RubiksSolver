import re
from face import *
from part import *
import random
import copy

colorMap = {                        # This map is used to initialize face colors when the cube is first made
        0 : "w",
        1 : "g", 
        2 : "r", 
        3 : "b", 
        4 : "o", 
        5 : "y"
        }

rotMap = {                          # This map is used to find out which face to rotate for the corresponding move
        "U": (0,True),  
        "u": (0,False),
        "L": (1,True),
        "l": (1,False),
        "F": (2,True),
        "f": (2,False),
        "R": (3,True),
        "r": (3,False),
        "B": (4,True),
        "b": (4,False),
        "D": (5,True),
        "d": (5,False)
        }

revMap = {                          # This map is used to reverse moves. When a move is made, the reverse move is appended to the self.history stack
        "U": "u",
        "u": "U",
        "L": "l",
        "l": "L",
        "F": "f",
        "f": "F",
        "R": "r",
        "r": "R",
        "B": "b",
        "b": "B",
        "D": "d",
        "d": "D"
        }

whiteCrossMoves = ["RDr","Rdr", "rDR","rdR", "LDl","Ldl",  "lDL","ldL", "FDf","Fdf",  "fDF","fdF",  "BDb","Bdb", "bDB","bdB"]

firstEdgeMoves = ["U","u","L","l","F","f","R","r","B","b","D","d"]#,"UU","LL","FF","RR","BB","DD"]
secondEdgeMoves = ["L","l","F","f","R","r","D","d"]#,"LL","FF","RR","DD"]
thirdEdgeMoves = ["L","l","F","f","D","d"]#,"LL","FF","DD"]
fourthEdgeMoves = ["L","l","D","d"]#,"LL","DD"]

whiteCornerMoves = ["D","d"]#,"DD"]

firstCornerMoves = ["rdRD","fdFD","ldLD","bdBD","FDfd","RDrd","BDbd","LDld","rDDRDrdR","fDDFDfdF","lDDLDldL","bDDBDbdB"]
secondCornerMoves = ["fdFD","ldLD","bdBD","RDrd","BDbd","LDld","fDDFDfdF","lDDLDldL","bDDBDbdB"]
thirdCornerMoves = ["fdFD","ldLD","BDbd","LDld","fDDFDfdF","lDDLDldL"]
fourthCornerMoves = ["fdFD","LDld","fDDFDfdF"]

middleLayerMoves = ["D","d"]

firstMiddleMoves = ["rdRDFDf", "bdBDRDr", "ldLDBDb", "fdFDLDl", "LDldfdF", "BDbdldL", "RDrdbdB", "FDfdrdR"]
secondMiddleMoves = ["bdBDRDr", "ldLDBDb", "fdFDLDl", "LDldfdF", "BDbdldL", "RDrdbdB"]
thirdMiddleMoves = ["ldLDBDb", "fdFDLDl", "LDldfdF", "BDbdldL"]
fourthMiddleMoves = ["fdFDLDl", "LDldfdF"]


#secondLayerMoves = ["LDKSGSF","ESRDFDG"]

yellowCrossMoves = []




class facet:                                                                # Every cell of the cube is called a facet, regardless of type of piece
    def __init__(self, color) -> None:                                      # Main cube structure is occupied by these facect objects
        self.color = color
        self.parent = None
        self.faces = [0]*6                                                  # This array shows all the colors that are in the parent piece that this edge is a part of
                                                                            # Follows same structure as colorMap

    def isSame(self, other):
        return self.color == other.color and self.faces == other.faces      # Two facets of different cubes can represent the same piece if the face color and faces list are the same

    def isSameColor(self,other):
        return self.color == other.color


class node:                                             # Nodes are used when the graph is generated for pathfinding
    def __init__(self,pos) -> None:                     # Node graph is strored in self.solveGraph map
        self.pos = pos
        self.changeList = dict()                        # change list maps every move to the node at the resulting location
        self.parent = None
        self.parentMove = ""
        self.score = 0
        

'''class change:                                           
    def __init__(self, move, targetNode) -> None:       # every node has a list of changes based on the moves stored in the graph
        #self.parent = None                              # previous edge
        #self.move = move                                # The move itself will be used for backtracking purposes
        self.targetNode = targetNode                    # node at new location resulting from the move
'''

class cube:
    def __init__(self) -> None:
        
        self.cubeArr = []                                               # Main cube structure
        self.populateCube()
        self.faceArr = [face(i, self.cubeArr) for i in range(6)]        # List of face objects used for rotation
        self.startArr = copy.deepcopy(self.cubeArr)                     # Copy of cube that is treated as solved state
        
        
        #self.pieceList = []
        #self.populatePieces()


        
        self.history = []                                               # Used for reversing moves
        self.solution = []
        self.solutionLength = 0
        self.solveGraph = dict()                                        # Graph used for backtracking
        self.initializeGraph()

        self.addAlgorithms()
        return None

    '''def populatePieces(self):

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
        self.pieceList.append(corner(19, (4,2,0),(5,2,2),(3,2,2)))'''

    def populateCube(self):
        for i in  range(6):
            self.cubeArr.append([[None]* 3 for i in range(3)])

        for currFace in range(6):
            for row in range(3):
                for col in range(3):
                    tempFacet = facet(colorMap[currFace])               # Every cell in 3D array is populated with a facet object
                    self.cubeArr[currFace][row][col] = tempFacet
        
    
    def resetCube(self):                                                # Resets Cube to solved state (Cheating, not actually solving)
        del self.cubeArr
        self.cubeArr = self.startArr
        self.startArr = copy.deepcopy(self.cubeArr)


    
    def printCube(self,cube):

        print("\n")

        for i in range(len(cube[0])):
            print("     ",cube[0][i][0].color,cube[0][i][1].color,cube[0][i][2].color)

        for i in range(len(cube[1])):
            print(cube[1][i][0].color, cube[1][i][1].color, cube[1][i][2].color, \
                    cube[2][i][0].color,cube[2][i][1].color,cube[2][i][2].color, \
                    cube[3][i][0].color,cube[3][i][1].color,cube[3][i][2].color, \
                    cube[4][i][0].color,cube[4][i][1].color,cube[4][i][2].color)


        for i in range(len(cube[5])):
            print("     ",cube[5][i][0].color,cube[5][i][1].color,cube[5][i][2].color)

        print("\n")


    def turnCubeX(self, clockwise = True):                                                  # Turn Whole Cube around X axis
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
    

    def turnCubeZ(self, clockwise = True):                                              # Turn Whole Cube around Z axis
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

    
    def turnCubeY(self, clockwise = True):                                              # Turn Whole Cube around Y axis
        
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

    
    def singleMove(self,move,cube,reverse = False):
        
        for turn in move:
            if turn not in rotMap:
                print("INVALID")
                return
            targetFace, direction = rotMap[turn]                    # Retrieve the face and direction from map based on input
            self.faceArr[targetFace].rotate(cube, direction)
            if not reverse:
                self.history.append(revMap[turn])

    def reverseMove(self,s,cube):
        for moves in range(len(s)):
            self.singleMove(self.history.pop(),cube, True)          # Reversing moves uses the history stack initialized earlier

    
    def multipleMoves(self,moves,cube):                                  # Performs multiple moves from an array
        for move in moves:
            self.singleMove(move,cube)
    
    
    def scramble(self, numMoves,cube):                                   # Scrambles the cube by randomly performing a set number of moves
        for move in range(numMoves):
            key, val = random.choice(list(rotMap.items()))
            self.singleMove(key,cube)


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

    def findPiece(self, pos, cube1, cube2):                                                 # iterates through 3d array to find matching piece
        for currFace in range(6):                                                           # Can be improved maybe with another map? Hard to say
            for row in range(3):
                for col in range(3):
                    if cube1[pos[0]][pos[1]][pos[2]].isSame(cube2[currFace][row][col]):
                        return (currFace, row, col)
    
    def initializeGraph(self):

        for currFace in range(6):
            for row in range(3):
                for col in range(3):
                    self.solveGraph[(currFace,row,col)] = node((currFace,row,col))      # initialize map


    def generateGraph(self, moves):                                                     # Makes graph mapping index changes from a group of moves

        tempCube = copy.deepcopy(self.cubeArr)                                          # make temporaty cube

        for move in moves:
            
            self.singleMove(move,tempCube)                                              # perform the current move
            
            #self.printCube(tempCube)

            for currFace in range(6):                                                                           # iterate through cube 3d array
                for row in range(3):
                    for col in range(3):
                        if self.cubeArr[currFace][row][col].isSame(tempCube[currFace][row][col]) == False:      # check if the facet is different from before
                            newPos = self.findPiece((currFace,row,col), self.cubeArr, tempCube)                 # if not get the two nodes from the graph
                            currentNode = self.solveGraph[(currFace,row,col)]
                            targetNode = self.solveGraph[newPos]
                            #newChange = change(move, targetNode)                                                # make a change object in the first node whose target is the second node
                            currentNode.changeList[move] = targetNode                                            # add change object to the first nodes change map


            self.reverseMove(move,tempCube)                                             # reverse the current move

        del tempCube            # free memory


    def addAlgorithms(self):
        self.generateGraph(firstEdgeMoves)
        self.generateGraph(whiteCrossMoves)
        self.generateGraph(firstCornerMoves)
        self.generateGraph(firstMiddleMoves)

    def bfs(self, targetPos, moves):

        newQ = []
        visited = []
        front = None

        currPos = self.findPiece(targetPos,self.startArr,self.cubeArr)
        #print(currPos)
        #print(len(self.solveGraph[currPos].changeList))
        #for key in self.solveGraph[currPos].changeList:
        #    print(key)

        newQ.append(self.solveGraph[currPos])

        while len(newQ)>0:
            front = newQ[0]

            if front.pos == targetPos:
                break

            front = newQ.pop(0)

            visited.append(front)

            for move in moves:
                if move in front.changeList:
                    nextNode  = front.changeList[move]#.targetNode
                    if nextNode not in visited:
                        newQ.append(nextNode)
                        nextNode.parent = front
                        nextNode.parentMove = move
                        nextNode.score = len(move)
        

        if len(newQ)==0:
            return "NOT FOUND"

        backtrack = []

        while front.pos != currPos and front.pos!= None:
            backtrack.append(front.parentMove)
            front = front.parent 
            self.solutionLength +=front.score
        
        return backtrack[::-1]


    def solveCube(self):
        self.solveWhiteCross()
        self.solveWhiteCorners()
        self.solveMiddleLayer()
        self.solveYellowCross()
        self.solveYellowFace()
        self.solveYellowCorners()
        self.solveYellowEdges()

    
    def solveWhiteCross(self):

        testMoves = self.bfs((0,0,1),firstEdgeMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((0,1,2),secondEdgeMoves+whiteCrossMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((0,2,1),thirdEdgeMoves+whiteCrossMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((0,1,0),fourthEdgeMoves+whiteCrossMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves


    def solveWhiteCorners(self):
        testMoves = self.bfs((0,2,2),whiteCornerMoves+firstCornerMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((0,0,2),whiteCornerMoves+secondCornerMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((0,0,0),whiteCornerMoves+thirdCornerMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((0,2,0),whiteCornerMoves+fourthCornerMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

    def solveMiddleLayer(self):

        testMoves = self.bfs((2,1,2),middleLayerMoves+firstMiddleMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((3,1,2),middleLayerMoves+secondMiddleMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((4,1,2),middleLayerMoves+thirdMiddleMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves

        testMoves = self.bfs((1,1,2),middleLayerMoves+fourthMiddleMoves)
        self.multipleMoves(testMoves,self.cubeArr)
        self.solution+=testMoves
        
        return
    
    
    
    
    def solveYellowCross(self):
        return
    def solveYellowFace(self):
        return
    def solveYellowCorners(self):
        return
    def solveYellowEdges(self):
        return








    


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


newCube = cube()

#for key in newCube.solveGraph:
#    print(key, " ", len(newCube.solveGraph[key].changeList))

#for node in newCube.solveGraph:
#print(len(node.changeList))
#newCube.generateGraph("F")
#newCube.generateGraph("R")

#newCube.printCube(newCube.cubeArr)
newCube.scramble(20,newCube.cubeArr)
newCube.printCube(newCube.cubeArr)

newCube.solveCube()

print(newCube.solution)
print(newCube.solutionLength)
newCube.printCube(newCube.cubeArr)

'''newCube.printCube(newCube.cubeArr)
newCube.singleMove("RUE",newCube.cubeArr)
newCube.printCube(newCube.cubeArr)
newCube.reverseMove("RUE",newCube.cubeArr)
newCube.printCube(newCube.cubeArr)
'''
'''newCube.singleMove("RUE", newCube.cubeArr)
print("\n")

newCube.printCube(newCube.cubeArr)

newCube.reverseMove("RUE",newCube.cubeArr)
print("\n")

newCube.printCube(newCube.cubeArr)
newCube.resetCube()


for key in newCube.solveGraph:
    print(key, " ", len(newCube.solveGraph[key].changeList))
'''

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