import string
from tokenize import String
from typing import List, Tuple
from part import *
from face import *
from databases import *
import random
import copy
import heapq




class cube:
    def __init__(self) -> None:
        
        self.cubeArr = []                                               # Main cube structure
        self.populateCube()
        self.faceArr = [face(i, self.cubeArr) for i in range(6)]        # List of face objects used for rotation
        self.startArr = copy.deepcopy(self.cubeArr)                     # Copy of cube that is treated as solved state
        
        self.history = []                                               # Used for reversing moves
        self.scrambleMoves = []                                         # Stores scramble 
        self.solution = []                                              # Stores solution
        self.solutionString = ""
        self.solutionLength = 0
        
        self.solveGraph = dict()                                        # Graph used for backtracking
        self.initializeGraph()

        self.addAlgorithms()                                            # Populate Graph with all the rotation changes
        return None

    
    def populateCube(self) -> None:
        for i in  range(6):
            self.cubeArr.append([[None]* 3 for i in range(3)])

        for currFace in range(6):
            for row in range(3):
                for col in range(3):
                    tempFacet = facet(colorMap[currFace])               # Every cell in 3D array is populated with a facet object
                    self.cubeArr[currFace][row][col] = tempFacet


    def setFaces(self,cube):
        # edge1
        cube[0][0][1].faces[indexMap[cube[0][0][1].color]]+=1

        
    
    
    def resetCube(self) -> None:                                                # Resets Cube to solved state (Cheating, not actually solving)
        del self.cubeArr
        self.cubeArr = self.startArr
        self.startArr = copy.deepcopy(self.cubeArr)


    
    def printCube(self,cube) -> None:             # Prints cube on terminal

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





    ###################################    ROTATION   ####################################################

    def rotateFullCube(self, direction) -> None:
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


    def turnCubeX(self, clockwise = True) -> None:                                                  # Turn Whole Cube around X axis
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
    

    def turnCubeZ(self, clockwise = True) -> None:                                              # Turn Whole Cube around Z axis
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

    
    def turnCubeY(self, clockwise = True) -> None:                                              # Turn Whole Cube around Y axis
        
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

    
    def singleMove(self,move,cube,reverse = False) -> None:
        
        for turn in move:
            if turn not in rotMap:
                print("INVALID")
                return
            targetFace, direction = rotMap[turn]                    # Retrieve the face and direction from map based on input
            self.faceArr[targetFace].rotate(cube, direction)
            if not reverse:
                self.history.append(revMap[turn])


    def reverseMove(self,s,cube) -> None:
        for moves in range(len(s)):
            self.singleMove(self.history.pop(),cube, True)          # Reversing moves uses the history stack initialized earlier


    
    def multipleMoves(self,moves,cube) -> None:                                  # Performs multiple moves from an array
        for move in moves:
            self.singleMove(move,cube)
    
    
    def scramble(self, numMoves,cube) -> None:                                   # Scrambles the cube by randomly performing a set number of moves
        self.scrambleMoves = []
        

        for move in range(numMoves):
            key, val = random.choice(list(rotMap.items()))
            self.scrambleMoves.append(key)
            self.singleMove(key,cube)

    
    def manualScramble(self,cube,inputCube):
        for currFace in self.faceArr:
            self.manualScrambleFace(currFace,cube,inputCube[currFace.index])
        for currFace in self.faceArr:
            currFace.setFacetParents(cube)
    
    
    def manualScrambleFace(self, currFace, cube, inputFace) -> None:             # Manual scramble
        for row in range(len(cube[currFace.index])):
            for col in range(len(cube[currFace.index][0])):
                cube[currFace.index][row][col].color = inputFace[row][col]
                cube[currFace.index][row][col].faces = [0]*6







    ###################################  GRAPH PATHFINDING   ####################################################




    def findPiece(self, pos, cube1, cube2) -> tuple[int,int,int]:                                                 # iterates through 3d array to find matching piece
        for currFace in range(6):                                                           # Can be improved maybe with another map? Hard to say
            for row in range(3):
                for col in range(3):
                    if cube1[pos[0]][pos[1]][pos[2]].isSame(cube2[currFace][row][col]):
                        return (currFace, row, col)
        print("NOT FOUND")
    
    
    def initializeGraph(self) -> None:
        for currFace in range(6):
            for row in range(3):
                for col in range(3):
                    self.solveGraph[(currFace,row,col)] = node((currFace,row,col),float("inf"))      # initialize map

    def resetGraph(self) -> None:
        for currFace in range(6):
            for row in range(3):
                for col in range(3):
                    self.solveGraph[(currFace,row,col)].score = float("inf")      # reset Map
                    self.solveGraph[(currFace,row,col)].parent = None


    def generateGraph(self, moves) -> None:                                                     # Makes graph mapping index changes from a group of moves

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


    def changeFront(self, rotations, inputList) -> None:         # Takes Algorithm and returns the same algorithm after the front is changed with a whole cube rotation
        
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

    
    
    
    def addAlgorithms(self) -> None:                                                                                    # Populates graph from function above with all the changes from each set of algorithms
        self.generateGraph(whiteCrossStandard + self.changeFront(["Z","ZZ","z"],whiteCrossStandard))
        self.generateGraph(whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCrossAdditional))
        self.generateGraph(whiteCornerStandard + self.changeFront(["Z","ZZ","z"],whiteCornerStandard))
        self.generateGraph(middleLayerStandard + self.changeFront(["Z","ZZ","z"],middleLayerStandard))
        self.generateGraph(yellowCrossStandard + self.changeFront(["Z","ZZ","z"],yellowCrossStandard))
        self.generateGraph(yellowFaceStandard + self.changeFront(["Z","ZZ","z"],yellowFaceStandard))
        self.generateGraph(yellowCornersStandard + self.changeFront(["Z","ZZ","z"],yellowCornersStandard))
        self.generateGraph(yellowEdgesStandard + self.changeFront(["Z","ZZ","z"],yellowEdgesStandard))

    

    def shortestPath(self, targetPos, moves) -> list[string]:

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

            #heapq.heappop(priorityQ)
            priorityQ.pop(0)
            heapq.heapify(priorityQ)
            

        


        if len(priorityQ)==0:
            return "NOT FOUND"

        self.solutionLength += front.score

        backtrack = []

        while True:
            if front == None:
                #print("None case")
                break
            elif front == self.solveGraph[currPos]:
                #print("match case")
                break
            backtrack.append(front.parentMove)
            front = front.parent 
            
    
        return backtrack[::-1]


    
    
    '''def shortestPath(self, targetPos, moves) -> list[string]:

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


    def solveCube(self) -> None:
        self.solution = []
        self.solutionString = ""

        self.solveWhiteCross()
        #print("cross done")
        self.solveWhiteCorners()
        #print("corners done")
        self.solveMiddleLayer()
        #print("middles done")
        self.solveYellowCross()
        #print("top cross done")
        self.solveYellowFace()
        #print("top face done")
        self.solveYellowCorners()
        #print("top corners done")
        self.solveYellowEdges()
        #print("cube done")

        self.printCube(self.cubeArr)
        self.solutionString = self.solutionString.join(self.solution)
        self.removeDuplicates(self.solutionString)




    
    def solveWhiteCross(self) -> None:

        # First Edge
        currMoves = self.shortestPath((0,0,1),whiteCrossStandard + self.changeFront(["Z","ZZ","z"],whiteCrossStandard) + whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCornerAdditional))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Second Edge
        currMoves = self.shortestPath((0,1,2),whiteCrossStandard + self.changeFront(["Z","ZZ"],whiteCrossStandard) + whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCornerAdditional))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Third Edge
        currMoves = self.shortestPath((0,2,1),whiteCrossStandard + self.changeFront(["Z"],whiteCrossStandard) + whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCornerAdditional))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Fourth Edge
        currMoves = self.shortestPath((0,1,0),whiteCrossStandard + whiteCrossAdditional + self.changeFront(["Z","ZZ","z"],whiteCrossAdditional))
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves


    def solveWhiteCorners(self) -> None:

        # First Corner
        currMoves = self.shortestPath((0,2,2), whiteCornerStandard + self.changeFront(["Z","ZZ","z"],whiteCornerStandard) + whiteCornerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Second Corner
        currMoves = self.shortestPath((0,0,2), whiteCornerStandard + self.changeFront(["z","ZZ"],whiteCornerStandard) + whiteCornerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Third Corner
        currMoves = self.shortestPath((0,0,0), whiteCornerStandard + self.changeFront(["z"],whiteCornerStandard) + whiteCornerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Fourth Corner
        currMoves = self.shortestPath((0,2,0), whiteCornerStandard + whiteCornerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

    
    def solveMiddleLayer(self) -> None:

        # First Edge
        currMoves = self.shortestPath((2,1,2), middleLayerStandard + self.changeFront(["Z","ZZ","z"], middleLayerStandard) + middleLayerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Second Edge
        currMoves = self.shortestPath((3,1,2), middleLayerStandard + self.changeFront(["ZZ","z"], middleLayerStandard) + middleLayerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Third Edge
        currMoves = self.shortestPath((4,1,2), middleLayerStandard + self.changeFront(["z"], middleLayerStandard) + middleLayerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        # Fourth Edge
        currMoves = self.shortestPath((1,1,2), middleLayerStandard + middleLayerAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves
        
        return


    def findSmallesStrings(self, listStrings) -> string:              # Helper Function
        
        smallest = listStrings[0]
        for currString in listStrings:
            if len(currString)<len(smallest):
                smallest = currString
        return smallest

    
    
    def solveYellowCross(self) -> None:

        
        # Orient first edge

        choiceArray = ["","","",""]
        listStrings = []

        listStrings.append(choiceArray[0].join(self.shortestPath((5,0,1), yellowCrossStandard + self.changeFront(["Z","ZZ","z"],yellowCrossStandard) + yellowCrossAdditional)))
        listStrings.append(choiceArray[1].join(self.shortestPath((5,1,2), yellowCrossStandard + self.changeFront(["Z","ZZ","z"],yellowCrossStandard) + yellowCrossAdditional)+["d"]))
        listStrings.append(choiceArray[2].join(self.shortestPath((5,2,1), yellowCrossStandard + self.changeFront(["Z","ZZ","z"],yellowCrossStandard) + yellowCrossAdditional)+["dd"]))
        listStrings.append(choiceArray[3].join(self.shortestPath((5,1,0), yellowCrossStandard + self.changeFront(["Z","ZZ","z"],yellowCrossStandard) + yellowCrossAdditional)+["D"]))

        currMoves = self.findSmallesStrings(listStrings)

        #currMoves = self.shortestPath((5,0,1), yellowCrossStandard + self.changeFront(["Z","ZZ","z"],yellowCrossStandard) + yellowCrossAdditional)
        self.multipleMoves([currMoves],self.cubeArr)
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


    def solveYellowFace(self) -> None:

        # Orient first corner

        choiceArray = ["","","",""]
        listStrings = []

        listStrings.append(choiceArray[0].join(self.shortestPath((5,0,0), yellowFaceStandard + self.changeFront(["Z","ZZ","z"],yellowFaceStandard) + yellowFaceAdditional)))
        listStrings.append(choiceArray[1].join(self.shortestPath((5,0,2), yellowFaceStandard + self.changeFront(["Z","ZZ","z"],yellowFaceStandard) + yellowFaceAdditional)+ ["d"]))
        listStrings.append(choiceArray[2].join(self.shortestPath((5,2,2), yellowFaceStandard + self.changeFront(["Z","ZZ","z"],yellowFaceStandard) + yellowFaceAdditional)+ ["dd"]))
        listStrings.append(choiceArray[3].join(self.shortestPath((5,2,0), yellowFaceStandard + self.changeFront(["Z","ZZ","z"],yellowFaceStandard) + yellowFaceAdditional)+ ["D"]))

        currMoves = self.findSmallesStrings(listStrings)
        
        #currMoves = self.shortestPath((5,0,0), yellowFaceStandard + self.changeFront(["Z","ZZ","z"],yellowFaceStandard) + yellowFaceAdditional)
        
        self.multipleMoves([currMoves],self.cubeArr)
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

        currMoves = self.shortestPath((5,0,2), yellowCornersAdditional)      # Position first corner
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        currMoves = self.shortestPath((5,0,0), yellowCornersStandard)        # Position adjacent corner
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        if (self.cubeArr[5][2][0].isSame(self.startArr[5][2][0]) == True and \
            self.cubeArr[5][2][2].isSame(self.startArr[5][2][2]) == True):      # Position last 2 corners
            return

        currMoves = self.changeFront(["ZZ"],["lFlBBLflBBLLD"])  
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        currMoves = self.shortestPath((5,0,0), yellowCornersAdditional)
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        return


    def solveYellowEdges(self) -> None:

        currMoves = self.shortestPath((5,0,1), yellowEdgesStandard + self.changeFront(["Z","ZZ","z"],yellowEdgesStandard))   # Position first edge
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves

        currMoves = self.shortestPath((5,1,2), self.changeFront(["Z"],yellowEdgesStandard))              # Position last 3 edges
        self.multipleMoves(currMoves,self.cubeArr)
        self.solution+=currMoves


        return

    def removeDuplicates(self, inputString):
        tempList = list(inputString)
        rsltList = []
        if len(tempList) <2:
            return tempList
        
        left = 0
        right = 1

        while right<len(tempList):

            if tempList[left] == tempList[right]:
                tempStr = tempList[left]+tempList[left]
                rsltList.append(tempStr)
                left = right
                right += 1
            
            else:
                rsltList.append(tempList[left])
            
            left += 1
            right += 1
        
        if  tempList[-1] != tempList[-2]:
            rsltList.append(tempList[-1])

        self.solution = rsltList
        return rsltList







