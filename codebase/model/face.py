from part import *

class face:

    def __init__(self, index) -> None:
        
        self.index = index
        self.neighbors = []
        self.reversedNeighbors = []
        self.populateNeighbors()
        return None
    
    def populateNeighbors(self):
        match self.index:
            case 0:
                self.neighbors = [(4,"u"),(3,"u"),(2,"u"),(1,"u")]
            case 1:
                self.neighbors = [(0,"l"),(2,"l"),(5,"l"),(4,"r")]
            case 2:
                self.neighbors = [(0,"d"),(3,"l"),(5,"u"),(1,"r")]
            case 3:
                self.neighbors = [(0,"r"),(4,"l"),(5,"r"),(2,"r")]
            case 4:
                self.neighbors = [(0,"u"),(1,"l"),(5,"d"),(3,"r")]
            case 5:
                self.neighbors = [(1,"d"),(2,"d"),(3,"d"),(4,"d")]
        
        self.reversedNeighbors = self.neighbors[::-1]


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

    def rotateFace(self, cube, clockwise = True):
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

    
    def rotateSides(self,cube, clockwise = True):

        path = self.neighbors if clockwise else self.reversedNeighbors
        
        prevArray = [0,0,0]
        currArray = [0,0,0]

        for idx in range(len(path)+1):
            idx = idx % len(path)
            faceVal = path[idx][0]
            
            if path[idx][1] == "l":

                currArray[0] = cube[faceVal][2][0]
                currArray[1] = cube[faceVal][1][0]
                currArray[2] = cube[faceVal][0][0]

                cube[faceVal][2][0] = prevArray[0]
                cube[faceVal][1][0] = prevArray[1]
                cube[faceVal][0][0] = prevArray[2]

            elif path[idx][1] == "r":
                currArray[0] = cube[faceVal][0][2]
                currArray[1] = cube[faceVal][1][2]
                currArray[2] = cube[faceVal][2][2]

                cube[faceVal][0][2] = prevArray[0]
                cube[faceVal][1][2] = prevArray[1]
                cube[faceVal][2][2] = prevArray[2]

            elif path[idx][1] == "u":
                currArray[0] = cube[faceVal][0][0]
                currArray[1] = cube[faceVal][0][1]
                currArray[2] = cube[faceVal][0][2]

                cube[faceVal][0][0] = prevArray[0]
                cube[faceVal][0][1] = prevArray[1]
                cube[faceVal][0][2] = prevArray[2]

            elif path[idx][1] == "d":
                currArray[0] = cube[faceVal][2][2]
                currArray[1] = cube[faceVal][2][1]
                currArray[2] = cube[faceVal][2][0]

                cube[faceVal][2][2] = prevArray[0]
                cube[faceVal][2][1] = prevArray[1]
                cube[faceVal][2][0] = prevArray[2]

            prevArray = currArray.copy() #if clockwise else currArray[::-1].copy()
