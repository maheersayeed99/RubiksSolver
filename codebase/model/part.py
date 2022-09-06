class part:
    def __init__(self) -> None:
        return None

class edge(part):

    def __init__(self) -> None:
        
        super().__init__()

        self.corner1 = None
        self.corner2 = None
        self.center1 = None
        self.center2 = None
        
        return None

class corner(part):
    def __init__(self) -> None:
        super().__init__()

        self.edge1 = None
        self.edge2 = None
        self.edge3 = None

        return None


class center(part):
    def __init__(self) -> None:
        super().__init__()
        self.edge1 = None
        self.edge2 = None
        self.edge3 = None
        self.edge4 = None
        return None



newCen = center()