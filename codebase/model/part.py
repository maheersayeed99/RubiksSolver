class part:
    def __init__(self) -> None:
        self.facets = []
        return None


    def isSame(self, cubeCurr, cubeEnd) -> bool:
        for face in self.facets:
            if cubeCurr[face[0]][face[1]][face[2]] != \
                cubeEnd[face[0]][face[1]][face[2]]:
                return False
        return True
        

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
