class part:
    def __init__(self) -> None:
        self.facets = []
        return None

    #def checkSame(self, cubeCurr, cubeEnd):
    #    for facet in self.facets


    def locate(self, otherPiece, cubeCurr, cubeEnd):
        if len(self.facets)!= len(otherPiece.facets):
            return False
        
        colorsCurr = []
        colorsEnd = []
        for idx in range(len(self.facets)):
            facet1 = self.facets[idx]
            facet2 = otherPiece.facets[idx]

            colorsCurr.append(cubeCurr[facet1[0]][facet1[1]][facet1[2]])
            colorsEnd.append(cubeEnd[facet2[0]][facet2[1]][facet2[2]])

        return sorted(colorsCurr) == sorted(colorsEnd)
        
        

class edge(part):

    def __init__(self, index, side1, side2) -> None:
        
        super().__init__()

        self.facets.append(side1)
        self.facets.append(side2)
        
        return None

class corner(part):
    def __init__(self, index, side1, side2, side3) -> None:
        super().__init__()

        self.facets.append(side1)
        self.facets.append(side2)
        self.facets.append(side3)

        return None
