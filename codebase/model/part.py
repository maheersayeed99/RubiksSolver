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
        
