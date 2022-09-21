from databases import *

edgeMap = {
    0:(0,1),
    1:(1,2),
    2:(2,1),
    3:(1,0),
}

upCornerMap = {
    0: (0,0),
    1: (0,2),
    2: (2,2),
    3: (2,0)
}

downCornerMap = {
    0: (0,2),
    1: (2,2),
    2: (2,0),
    3: (0,0)
}



class face:

    def __init__(self, index, cube) -> None:
        
        self.index = index
        self.neighbors = []
        self.reversedNeighbors = []
        self.populateNeighbors()
        self.setFacetParents(cube)
        
        return None
    
    def populateNeighbors(self):                                    # Hard coded to identify neighbors for rotation purposes
        match self.index:
            
            case 0:
                self.neighbors = [(4,0),(3,0),(2,0),(1,0)]
            case 1:
                self.neighbors = [(0,3),(2,3),(5,3),(4,1)]
            case 2:
                self.neighbors = [(0,2),(3,3),(5,0),(1,1)]
            case 3:
                self.neighbors = [(0,1),(4,3),(5,1),(2,1)]
            case 4:
                self.neighbors = [(0,0),(1,3),(5,2),(3,1)]
            case 5:
                #self.neighbors = [(1,2),(2,2),(3,2),(4,2)]
                self.neighbors = [(2,2),(3,2),(4,2),(1,2)]

        self.reversedNeighbors = self.neighbors[::-1]           # Needed for counter clockwise rotation




    '''def setFacetParents(self,cube):                                 # This is done so each facet identifies with the other facets in its piece
        #center
        cube[self.index][1][1].faces[self.index]+=1
        # up edge
        cube[self.index][0][1].faces[self.index]+=1
        cube[self.index][0][1].faces[self.neighbors[0][0]]+=1
        # right edge
        cube[self.index][1][2].faces[self.index]+=1
        cube[self.index][1][2].faces[self.neighbors[1][0]]+=1
        # down edge
        cube[self.index][2][1].faces[self.index]+=1
        cube[self.index][2][1].faces[self.neighbors[2][0]]+=1
        # left edge
        cube[self.index][1][0].faces[self.index]+=1
        cube[self.index][1][0].faces[self.neighbors[3][0]]+=1
        # up right corner
        cube[self.index][0][2].faces[self.index]+=1
        cube[self.index][0][2].faces[self.neighbors[0][0]]+=1
        cube[self.index][0][2].faces[self.neighbors[1][0]]+=1
        # down right corner
        cube[self.index][2][2].faces[self.index]+=1
        cube[self.index][2][2].faces[self.neighbors[2][0]]+=1
        cube[self.index][2][2].faces[self.neighbors[1][0]]+=1
        # down left corner
        cube[self.index][2][0].faces[self.index]+=1
        cube[self.index][2][0].faces[self.neighbors[2][0]]+=1
        cube[self.index][2][0].faces[self.neighbors[3][0]]+=1
        # up left corner
        cube[self.index][0][0].faces[self.index]+=1
        cube[self.index][0][0].faces[self.neighbors[0][0]]+=1
        cube[self.index][0][0].faces[self.neighbors[3][0]]+=1'''

    def setFacetParents(self,cube):                                 # This is done so each facet identifies with the other facets in its piece
        #center
        #cube[self.index][1][1].faces[self.index]+=1
        cube[self.index][1][1].faces[indexMap[cube[self.index][1][1].color]]+=1
        
        # up edge
        cube[self.index][0][1].faces[indexMap[cube[self.index][0][1].color]]+=1
        cube[self.index][0][1].faces[indexMap[cube[self.neighbors[0][0]][edgeMap[self.neighbors[0][1]][0]][edgeMap[self.neighbors[0][1]][1]].color]]+=1
        # right edge
        cube[self.index][1][2].faces[indexMap[cube[self.index][1][2].color]]+=1
        cube[self.index][1][2].faces[indexMap[cube[self.neighbors[1][0]][edgeMap[self.neighbors[1][1]][0]][edgeMap[self.neighbors[1][1]][1]].color]]+=1
        # down edge
        cube[self.index][2][1].faces[indexMap[cube[self.index][2][1].color]]+=1
        cube[self.index][2][1].faces[indexMap[cube[self.neighbors[2][0]][edgeMap[self.neighbors[2][1]][0]][edgeMap[self.neighbors[2][1]][1]].color]]+=1
        # left edge
        cube[self.index][1][0].faces[indexMap[cube[self.index][1][0].color]]+=1
        cube[self.index][1][0].faces[indexMap[cube[self.neighbors[3][0]][edgeMap[self.neighbors[3][1]][0]][edgeMap[self.neighbors[3][1]][1]].color]]+=1
        
        
        
        
        
        
        
        # up right corner
        cube[self.index][0][2].faces[indexMap[cube[self.index][0][2].color]]+=1
        cube[self.index][0][2].faces[indexMap[cube[self.neighbors[0][0]][upCornerMap[self.neighbors[0][1]][0]][upCornerMap[self.neighbors[0][1]][1]].color]]+=1
        cube[self.index][0][2].faces[indexMap[cube[self.neighbors[1][0]][downCornerMap[self.neighbors[1][1]][0]][downCornerMap[self.neighbors[1][1]][1]].color]]+=1



        #cube[self.index][0][2].faces[self.neighbors[0][0]]+=1
        #cube[self.index][0][2].faces[self.neighbors[1][0]]+=1
        
        
        
        
        # down right corner
        cube[self.index][2][2].faces[indexMap[cube[self.index][2][2].color]]+=1
        
        #cube[self.index][2][2].faces[self.neighbors[2][0]]+=1
        #cube[self.index][2][2].faces[self.neighbors[1][0]]+=1
        cube[self.index][2][2].faces[indexMap[cube[self.neighbors[1][0]][upCornerMap[self.neighbors[1][1]][0]][upCornerMap[self.neighbors[1][1]][1]].color]]+=1
        # Facet at cell
        #                       access faces
        #                            Use index map to convert color to index
        #                                       Second entry in neighbors is down, right, so correct face index
        #                                                                Second and third index is taken from downCornerMap with direction 
        cube[self.index][2][2].faces[indexMap[cube[self.neighbors[2][0]][downCornerMap[self.neighbors[2][1]][0]][downCornerMap[self.neighbors[2][1]][1]].color]]+=1
        
        
        
        
        
        
        # down left corner
        cube[self.index][2][0].faces[indexMap[cube[self.index][2][0].color]]+=1
        
        #cube[self.index][2][0].faces[self.neighbors[2][0]]+=1
        #cube[self.index][2][0].faces[self.neighbors[3][0]]+=1
        
        cube[self.index][2][0].faces[indexMap[cube[self.neighbors[2][0]][upCornerMap[self.neighbors[2][1]][0]][upCornerMap[self.neighbors[2][1]][1]].color]]+=1
        cube[self.index][2][0].faces[indexMap[cube[self.neighbors[3][0]][downCornerMap[self.neighbors[3][1]][0]][downCornerMap[self.neighbors[3][1]][1]].color]]+=1
        
        
        
        
        # up left corner
        cube[self.index][0][0].faces[indexMap[cube[self.index][0][0].color]]+=1
        
        #cube[self.index][0][0].faces[self.neighbors[0][0]]+=1
        #cube[self.index][0][0].faces[self.neighbors[3][0]]+=1


        cube[self.index][0][0].faces[indexMap[cube[self.neighbors[3][0]][upCornerMap[self.neighbors[3][1]][0]][upCornerMap[self.neighbors[3][1]][1]].color]]+=1
        cube[self.index][0][0].faces[indexMap[cube[self.neighbors[0][0]][downCornerMap[self.neighbors[0][1]][0]][downCornerMap[self.neighbors[0][1]][1]].color]]+=1

    


    def rotate(self, cube, clockwise = True):
        self.rotateFace(cube, clockwise)
        self.rotateSides(cube, clockwise)
    
    # transpose with reverse means counter clockwise rotation
    #   1 2 3   1 4 7   3 6 9
    #   4 5 6   2 5 8   2 5 8
    #   7 8 9   3 6 9   1 4 7

    # reverse with transpose means clockwise rotation
    #   1 2 3   7 8 9   7 4 1
    #   4 5 6   4 5 6   8 5 2
    #   7 8 9   1 2 3   9 6 3

    def rotateFace(self, cube, clockwise = True):           # in place rotation algorithm
        currFace = cube[self.index]
        if clockwise == True:
            currFace.reverse()
            self.transpose(cube)
        else:
            self.transpose(cube)
            currFace.reverse()

    def transpose(self, cube):
        currFace = cube[self.index]
        rows = len(currFace)
        cols = len(currFace[0])

        for row in range(rows):
            for col in range(row, cols):
                currFace[row][col],currFace[col][row] = \
                currFace[col][row], currFace[row][col]

    
    def rotateSides(self,cube, clockwise = True):                           # Sliding window technique used

        path = self.neighbors if clockwise else self.reversedNeighbors
        
        prevArray = [0,0,0]
        currArray = [0,0,0]

        for idx in range(len(path)+1):
            idx = idx % len(path)
            faceVal = path[idx][0]
            
            if path[idx][1] == 3:

                currArray[0] = cube[faceVal][2][0]
                currArray[1] = cube[faceVal][1][0]
                currArray[2] = cube[faceVal][0][0]

                cube[faceVal][2][0] = prevArray[0]
                cube[faceVal][1][0] = prevArray[1]
                cube[faceVal][0][0] = prevArray[2]

            elif path[idx][1] == 1:
                currArray[0] = cube[faceVal][0][2]
                currArray[1] = cube[faceVal][1][2]
                currArray[2] = cube[faceVal][2][2]

                cube[faceVal][0][2] = prevArray[0]
                cube[faceVal][1][2] = prevArray[1]
                cube[faceVal][2][2] = prevArray[2]

            elif path[idx][1] == 0:
                currArray[0] = cube[faceVal][0][0]
                currArray[1] = cube[faceVal][0][1]
                currArray[2] = cube[faceVal][0][2]

                cube[faceVal][0][0] = prevArray[0]
                cube[faceVal][0][1] = prevArray[1]
                cube[faceVal][0][2] = prevArray[2]

            elif path[idx][1] == 2:
                currArray[0] = cube[faceVal][2][2]
                currArray[1] = cube[faceVal][2][1]
                currArray[2] = cube[faceVal][2][0]

                cube[faceVal][2][2] = prevArray[0]
                cube[faceVal][2][1] = prevArray[1]
                cube[faceVal][2][0] = prevArray[2]

            prevArray = currArray.copy() #if clockwise else currArray[::-1].copy()
