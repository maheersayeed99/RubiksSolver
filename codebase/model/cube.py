from queue import PriorityQueue
from face import *
import random
import copy
import heapq

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
        "d": "D",
        "X": "x",
        "Y": "y",
        "Z": "z",
        "x": "X",
        "y": "Y",
        "z": "Z"
        }

# All the algorithms for each step of solving the cube        

whiteCrossStandard = ["L","l","D","d"]
whiteCrossAdditional = ["RDr","Rdr", "rDR","rdR"]
whiteCornerStandard = ["fdFD","LDld","fDDFDfdF"]
whiteCornerAdditional = ["D","d"]
middleLayerStandard = ["fdFDLDl", "LDldfdF"]
middleLayerAdditional = ["D","d"]
yellowCrossStandard = ["FDLdlf","FLDldf"]
yellowCrossAdditional = ["D","d"]
yellowFaceStandard = ["LDlDLDDl"]
yellowFaceAdditional = ["D","d"]
yellowCornersStandard = ["lFlBBLflBBLL"]
yellowCornersAdditional = ["D","d"]
yellowEdgesStandard = ["RRdBfRRbFdRR"]




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
    def __init__(self,pos, score) -> None:                     # Node graph is strored in self.solveGraph map
        self.pos = pos
        self.changeList = dict()                        # change list maps every move to the node at the resulting location
        self.parent = None
        self.parentMove = ""
        self.score = score

    def __lt__(self, other):
        return self.score < other.score
        

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
        
        self.history = []                                               # Used for reversing moves
        self.scrambleMoves = []                                         # Stores scramble 
        self.solution = []                                              # Stores solution
        self.solutionLength = 0
        
        self.solveGraph = dict()                                        # Graph used for backtracking
        self.initializeGraph()

        self.addAlgorithms()                                            # Populate Graph with all the rotation changes
        return None

    
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


    
    def printCube(self,cube):             # Prints cube on terminal

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



    def rotateFullCube(self, direction):
        if direction == "X":
            self.turnCubeX()
        elif direction == "x":
            self.turnCubeX(False)
        elif direction == "Y":
            self.turnCubeY()
        elif direction == "y":
            self.turnCubeY(False)
        elif direction == "Z":
            self.turnCubeZ()
        elif direction == "z":
            self.turnCubeZ(False)

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
        self.scrambleMoves = []
        for move in range(numMoves):
            key, val = random.choice(list(rotMap.items()))
            self.scrambleMoves.append(key)
            self.singleMove(key,cube)


    
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
                    self.solveGraph[(currFace,row,col)] = node((currFace,row,col),1000000)      # initialize map

    def resetGraph(self):
        for currFace in range(6):
            for row in range(3):
                for col in range(3):
                    self.solveGraph[(currFace,row,col)].score = 10000      # reset Map
                    self.solveGraph[(currFace,row,col)].parent = None


    def generateGraph(self, moves):                                                     # Makes graph mapping index changes from a group of moves

        tempCube = copy.deepcopy(self.cubeArr)                                          # make temporaty cube

        for move in moves:
            
            self.singleMove(move,tempCube)                                              # perform the current move

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


    def changeFront(self, rotations, inputList):         # Takes Algorithm and returns the same algorithm after the front is changed with a whole cube rotation
        
        moves = ["U","L","F","R","B","D"]
        movesMap = dict()
        changeMap = dict()

        rslt = []
        for rotation in rotations:

            for currFace in range(len(self.cubeArr)):
                movesMap[self.cubeArr[currFace][1][1]] = moves[currFace]                    # populate first map
                
            for wholeTurn in rotation: 
                self.rotateFullCube(wholeTurn)                                              # Rotate Cube

            for currFace in range(len(self.cubeArr)):
                changeMap[moves[currFace]] = movesMap[self.cubeArr[currFace][1][1]]         # populate second map
                
            for wholeTurn in rotation[::-1]:
                self.rotateFullCube(revMap[wholeTurn])                                      # Reverse Rotation

            currentRotationOutput =  []

            for move in inputList:
                
                currMoveString = ""

                for turn in move:

                    if turn.upper() != turn:
                        temp = changeMap[turn.upper()]          # Use second map to map input string to output string
                        currMoveString+= temp.lower()         # Account for clockwise/counterclockwise with .upper() and .lower()
                    
                    else:
                        currMoveString+= changeMap[turn]
                
                currentRotationOutput.append(currMoveString)
            
            rslt += currentRotationOutput

        return rslt

    
    
    
    def addAlgorithms(self):                                                                                    # Populates graph from function above with all the changes from each set of algorithms
        self.generateGraph(whiteCrossStandard + self.changeFront(["Z","ZZ","z"],whiteCrossStandard))
        self.generateGraph(whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCrossAdditional))
        self.generateGraph(whiteCornerStandard + self.changeFront(["Z","ZZ","z"],whiteCornerStandard))
        self.generateGraph(middleLayerStandard + self.changeFront(["Z","ZZ","z"],middleLayerStandard))
        self.generateGraph(yellowCrossStandard + self.changeFront(["Z","ZZ","z"],yellowCrossStandard))
        self.generateGraph(yellowFaceStandard + self.changeFront(["Z","ZZ","z"],yellowFaceStandard))
        self.generateGraph(yellowCornersStandard + self.changeFront(["Z","ZZ","z"],yellowCornersStandard))
        self.generateGraph(yellowEdgesStandard + self.changeFront(["Z","ZZ","z"],yellowEdgesStandard))

    

    def bfs(self, targetPos, moves):

        self.resetGraph()

        currPos = self.findPiece(targetPos,self.startArr,self.cubeArr)
        priorityQ = []
        visited = []
        front = None

        for key in self.solveGraph:
            if key == currPos:
                self.solveGraph[key].score = 0
            #print(self.solveGraph[key].score, " ", self.solveGraph[key])

            heapq.heappush(priorityQ, self.solveGraph[key])

            #heapq.heappush(heap, (1,checkNode1))
        i = 0
        while len(priorityQ)>0:
            i+=1
            print(i)
            if i == 10000:
                
                return "STUCK IN LOOP" 
            front = priorityQ[0]

            if front.pos == targetPos:
                break

            for move in moves:
                if move in front.changeList:
                    nextNode  = front.changeList[move]#.targetNode
                    if nextNode not in visited:
                        #print(len(move), " ", front.score)
                        currDist = len(move) + front.score
                        
                        if currDist < nextNode.score:
                            nextNode.parent = front
                            nextNode.parentMove = move
                            nextNode.score = currDist
                            priorityQ.append(nextNode)
                            #visited.append(nextNode)
                            
            visited.append(front)

            heapq.heappop(priorityQ)

        


        if len(priorityQ)==0:
            return "NOT FOUND"

        self.solutionLength = front.score

        print("exited loop")

        backtrack = []

        while front != None and front.pos != currPos and front.pos!= None:
            backtrack.append(front.parentMove)
            front = front.parent 
            
    
        return backtrack[::-1]


    
    
    '''def bfs(self, targetPos, moves):

        newQ = []
        visited = []
        front = None

        currPos = self.findPiece(targetPos,self.startArr,self.cubeArr)
        
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
        
        return backtrack[::-1]'''


    
    ###################################    SOLVE   ####################################################


    def solveCube(self):
        self.solveWhiteCross()
        print("cross done")
        self.solveWhiteCorners()
        print("corners done")
        self.solveMiddleLayer()
        print("middles done")
        self.solveYellowCross()
        print("top cross done")
        self.solveYellowFace()
        print("top face done")
        self.solveYellowCorners()
        print("top corners done")
        self.solveYellowEdges()
        print("cube done")

    
    def solveWhiteCross(self):

        # First Edge
        currMoves = self.bfs((0,0,1),whiteCrossStandard + self.changeFront(["Z","ZZ","z"],whiteCrossStandard) + whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCornerAdditional))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Second Edge
        currMoves = self.bfs((0,1,2),whiteCrossStandard + self.changeFront(["Z","ZZ"],whiteCrossStandard) + whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCornerAdditional))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Third Edge
        currMoves = self.bfs((0,2,1),whiteCrossStandard + self.changeFront(["Z"],whiteCrossStandard) + whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCornerAdditional))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Fourth Edge
        currMoves = self.bfs((0,1,0),whiteCrossStandard + whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCrossAdditional))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves


    def solveWhiteCorners(self):

        # First Corner
        currMoves = self.bfs((0,2,2), whiteCornerStandard + self.changeFront(["Z","ZZ","z"],whiteCornerStandard) + whiteCornerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Second Corner
        currMoves = self.bfs((0,0,2), whiteCornerStandard + self.changeFront(["z","ZZ"],whiteCornerStandard) + whiteCornerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Third Corner
        currMoves = self.bfs((0,0,0), whiteCornerStandard + self.changeFront(["z"],whiteCornerStandard) + whiteCornerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Fourth Corner
        currMoves = self.bfs((0,2,0), whiteCornerStandard + whiteCornerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

    
    def solveMiddleLayer(self):

        # First Edge
        currMoves = self.bfs((2,1,2), middleLayerStandard + self.changeFront(["Z","ZZ","z"], middleLayerStandard) + middleLayerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Second Edge
        currMoves = self.bfs((3,1,2), middleLayerStandard + self.changeFront(["ZZ","z"], middleLayerStandard) + middleLayerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Third Edge
        currMoves = self.bfs((4,1,2), middleLayerStandard + self.changeFront(["z"], middleLayerStandard) + middleLayerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Fourth Edge
        currMoves = self.bfs((1,1,2), middleLayerStandard + middleLayerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves
        
        return
    
    
    def solveYellowCross(self):

        currMoves = self.bfs((5,0,1), yellowCrossStandard + self.changeFront(["Z","ZZ","z"],yellowCrossStandard) + yellowCrossAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        if (self.cubeArr[5][1][0].isSameColor(self.startArr[5][1][0]) == True and \
            self.cubeArr[5][1][2].isSameColor(self.startArr[5][1][2]) == True):

            return
        
        elif self.cubeArr[5][1][2].isSameColor(self.startArr[5][1][2]) == True:
              #         L shape
              # #
            currMoves = self.changeFront(["z"],[yellowCrossStandard[0]]) #["LDBdbl"] 
            

        elif self.cubeArr[5][1][0].isSameColor(self.startArr[5][1][0]) == True:
                #       Backwards L shape
              # #

            currMoves = self.changeFront(["ZZ"],[yellowCrossStandard[0]])

        else: #if self.cubeArr[5][0][2].isSameColor(self.startArr[5][0][2]) == True:
            #           Vertical Line Shape
            #
            #

            currMoves = self.changeFront(["z"],[yellowCrossStandard[1]])
            
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

    def solveYellowFace(self):
        currMoves = self.bfs((5,0,0), yellowFaceStandard + self.changeFront(["Z","ZZ","z"],yellowFaceStandard) + yellowFaceAdditional)
        
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        if (self.cubeArr[5][0][2].isSameColor(self.startArr[5][0][2]) == True and \
            self.cubeArr[5][2][0].isSameColor(self.startArr[5][2][0]) == True and \
            self.cubeArr[5][2][2].isSameColor(self.startArr[5][2][2]) == True):

            # # #       Already Solved
            # # #
            # # #

            return

        elif (self.cubeArr[5][0][2].isSameColor(self.startArr[5][0][2]) == True and\
            self.cubeArr[3][2][2].isSameColor(self.startArr[5][2][2]) == True):
            
            # # #
            # # #
              #  #

            currMoves = ["BRfrbRFr"]
            
        elif (self.cubeArr[5][0][2].isSameColor(self.startArr[5][0][2]) == True and\
            self.cubeArr[4][2][0].isSameColor(self.startArr[5][2][2]) == True):
            
            # # #
            # # #
              #  
                #

            currMoves = ["rrUrDDRurDDr"]
            

        elif (self.cubeArr[5][2][0].isSameColor(self.startArr[5][2][0]) == True and\
            self.cubeArr[3][2][2].isSameColor(self.startArr[5][2][2]) == True):

            # # 
            # # #
            # #  #

            currMoves = self.changeFront(["z"], ["rrUrDDRurDDr"])
            
        elif (self.cubeArr[5][2][0].isSameColor(self.startArr[5][2][0]) == True and\
            self.cubeArr[4][2][0].isSameColor(self.startArr[5][2][2]) == True):
            
            # #
            # # #
            # # 
                #
            
            currMoves = self.changeFront(["z"], ["BRfrbRFr"])
        
        elif (self.cubeArr[5][2][2].isSameColor(self.startArr[5][2][2]) == True and\
            self.cubeArr[3][2][0].isSameColor(self.startArr[5][0][2]) == True):
            # #  #
            # # #
              # #
            #
            currMoves = ["rBRfrbRF"]
        
        elif (self.cubeArr[5][2][2].isSameColor(self.startArr[5][2][2]) == True and\
            self.cubeArr[2][2][2].isSameColor(self.startArr[5][0][2]) == True):
                #
            # #  
            # # #
          #   # #
            
            currMoves = self.changeFront(["ZZ"], ["rBRfrbRF"])

        elif (self.cubeArr[1][2][0].isSameColor(self.startArr[5][2][0]) == True):
            currMoves = ["BDbDBDDb"]

        else:
            currMoves = ["rdRdrDDR"]

        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves
            
            
    def solveYellowCorners(self):

        currMoves = self.bfs((5,0,2), yellowCornersAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        currMoves = self.bfs((5,0,0), yellowCornersStandard)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        if (self.cubeArr[5][2][0].isSame(self.startArr[5][2][0]) == True and \
            self.cubeArr[5][2][2].isSame(self.startArr[5][2][2]) == True):
            return

        currMoves = self.changeFront(["ZZ"],["lFlBBLflBBLLD"])  
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        currMoves = self.bfs((5,0,0), yellowCornersAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        return


    def solveYellowEdges(self):

        currMoves = self.bfs((5,0,1), yellowEdgesStandard + self.changeFront(["Z","ZZ","z"],yellowEdgesStandard))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        currMoves = self.bfs((5,1,2), self.changeFront(["Z"],yellowEdgesStandard))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves


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

newCube.scramble(100,newCube.cubeArr)
newCube.printCube(newCube.cubeArr)

newCube.solveCube()

rslt = ""
print(newCube.scrambleMoves)

rslt = rslt.join(newCube.solution)

print(newCube.solution)
print(len(rslt))
newCube.printCube(newCube.cubeArr)


print(newCube.changeFront(["z"],["R"]))
print(newCube.changeFront("Z","L"))


checkNode1 = node((0,1,2),1)
checkNode2 = node((0,0,2),1)
checkNode3 = node((0,1,0),2)
heap = []
heapq.heappush(heap, checkNode1)
heapq.heappush(heap, checkNode2)
heapq.heappush(heap, checkNode3)

print(heapq.heappop(heap).score)
print(heapq.heappop(heap).score)
print(heap[0].score)



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