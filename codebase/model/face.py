from part import *

class face:

    def __init__(self, index) -> None:
        
        self.index = index
        self.neighbors = []
        self.populateNeighbors()
        self.Up = None
        self.Down = None
        self.Left = None
        self.Right = None

        return None
    
    def populateNeighbors(self):
        match self.index:
            case 0:
                self.neighbors = [(4,"u"),(3,"u"),(2,"u"),(1,"u")]
                return
            case 1:
                self.neighbors = [(4,"r"),(5,"l"),(2,"l"),(0,"l")]
                return
            case 2:
                self.neighbors = [(3,"l"),(5,"u"),(1,"r"),(0,"d")]
                return
            case 3:
                self.neighbors = [(4,"l"),(5,"r"),(2,"r"),(0,"r")]
                return
            case 4:
                self.neighbors = [(3,"r"),(5,"d"),(1,"l"),(0,"u")]
                return
            case 5:
                self.neighbors = [(4,"d"),(3,"d"),(2,"d"),(1,"d")]
                return


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

    
    def rotateSides(self,cube):
        
        prev1 = prev2 = prev3 = 0

        for idx in range(len(self.neighbors)):
            faceVal = self.neighbors[idx][0]
            
            if self.neighbors[idx][1] == "l":
                
                curr1 = cube[faceVal][2][0]
                curr2 = cube[faceVal][1][0]
                curr3 = cube[faceVal][0][0]

                cube[faceVal][2][0] = prev1
                cube[faceVal][1][0] = prev2
                cube[faceVal][0][0] = prev3

                prev1, prev2, prev3 = curr1, curr2, curr3
                
            elif self.neighbors[idx][1] == "r":
                curr1 = cube[faceVal][0][2]
                curr2 = cube[faceVal][1][2]
                curr3 = cube[faceVal][2][2]

                cube[faceVal][0][2] = prev1
                cube[faceVal][1][2] = prev2
                cube[faceVal][2][2] = prev3

                prev1, prev2, prev3 = curr1, curr2, curr3

            elif self.neighbors[idx][1] == "u":
                curr1 = cube[faceVal][0][0]
                curr2 = cube[faceVal][0][1]
                curr3 = cube[faceVal][0][2]

                cube[faceVal][0][0] = prev1
                cube[faceVal][0][1] = prev2
                cube[faceVal][0][2] = prev3

                prev1, prev2, prev3 = curr1, curr2, curr3

            elif self.neighbors[idx][1] == "d":
                curr1 = cube[faceVal][2][2]
                curr2 = cube[faceVal][2][1]
                curr3 = cube[faceVal][2][0]

                cube[faceVal][2][2] = prev1
                cube[faceVal][2][1] = prev2
                cube[faceVal][2][0] = prev3
                
                prev1, prev2, prev3 = curr1, curr2, curr3

        faceVal = self.neighbors[0][0]
        match self.neighbors[0][1]:
            case "l":
                cube[faceVal][2][0] = prev1
                cube[faceVal][1][0] = prev2
                cube[faceVal][0][0] = prev3

            case "r":
                cube[faceVal][0][2] = prev1
                cube[faceVal][1][2] = prev2
                cube[faceVal][2][2] = prev3
            case "u":
                cube[faceVal][0][0] = prev1
                cube[faceVal][0][1] = prev2
                cube[faceVal][0][2] = prev3
                
            case "d": 
                cube[faceVal][2][2] = prev1
                cube[faceVal][2][1] = prev2
                cube[faceVal][2][0] = prev3

