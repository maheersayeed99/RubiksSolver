from part import *

class face:

    def __init__(self, index, cube) -> None:
        

        self.currFace = cube[index]
        self.neighbors = []

        return None


    # transpose with reverse means counter clockwise rotation
    #   1 2 3   1 4 7   3 6 9
    #   4 5 6   2 5 8   2 5 8
    #   7 8 9   3 6 9   1 4 7

    # reverse with transpose means clockwise rotation
    #   1 2 3   7 8 9   7 4 1
    #   4 5 6   4 5 6   8 5 2
    #   7 8 9   1 2 3   9 6 3

    def rotateFace(self, clockwise = True):
        if clockwise:
            self.currFace.reverse()
            self.transpose()
        else:
            self.transpose()
            self.currFace.reverse()

    def transpose(self):
        rows = len(self.currFace)
        cols = len(self.currFace[0])

        for row in range(rows):
            for col in range(row, cols):
                self.currFace[row][col],self.currFace[col][row] = \
                self.currFace[col][row], self.currFace[row][col]


