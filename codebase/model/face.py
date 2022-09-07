from part import *

class face:

    def __init__(self, index) -> None:
        
        self.index = index
        self.neighbors = []
        self.Up = None
        self.Down = None
        self.Left = None
        self.Right = None

        return None

    '''

    def populateNeighbors(self):
        match self.index:
            case 0:
                self.Up = ((),(),())
                self.Down = ((),(),())
                self.Left = ((),(),())
                self.Right = ((),(),())
                return
            case 1:
                return
            case 2:
                return
            case 3:
                return
            case 4:
                return
            case 5:
                return
            
        return None

    '''

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
'''
    def rotateSides(self):
        temp1,temp2,temp3 = cube[][][], cube[][][], cube[][][]
        cube[][][], cube[][][], cube[][][] = cube[][][], cube[][][], cube[][][]
        cube[][][], cube[][][], cube[][][] = cube[][][], cube[][][], cube[][][]
        cube[][][], cube[][][], cube[][][] = cube[][][], cube[][][], cube[][][]
        cube[][][], cube[][][], cube[][][] = temp1, temp2, temp3

'''
