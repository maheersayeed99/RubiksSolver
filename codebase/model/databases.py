

# This map is used to initialize face colors when the cube is first made
colorMap = {0 : "w",
            1 : "g", 
            2 : "r", 
            3 : "b", 
            4 : "o", 
            5 : "y"}

# This map is used to find out which face to rotate for the corresponding move
rotMap = {"U": (0,True),
        "u": (0,False),
        "L": (1,True),
        "l": (1,False),
        "F": (2,True),
        "f": (2,False),
        "R": (3,True),
        "r": (3,False),
        "B": (4,True),
        "b": (4,False),
        "D": (5,True),
        "d": (5,False)}

# This map is used to reverse moves. When a move is made, the reverse move is appended to the self.history stack
revMap = {"U": "u",
        "u": "U",
        "L": "l",
        "l": "L",
        "F": "f",
        "f": "F",
        "R": "r",
        "r": "R", 
        "B": "b",
        "b": "B",
        "D": "d",
        "d": "D", 
        "X": "x", 
        "Y": "y",
        "Z": "z",
        "x": "X",
        "y": "Y",
        "z": "Z"}

# All the algorithms for each step of solving the cube        

whiteCrossStandard = ["L","l","D","d"]
whiteCrossAdditional = ["RDr","RDDr","Rdr", "rDR", "rDDR", "rdR"]
whiteCornerStandard = ["fdF", "fddF", "LDl", "LDDl", "fDDFDfdF"]
whiteCornerAdditional = ["D","d"]
middleLayerStandard = ["fdFDLDl", "LDldfdF", "fddFDDLDl", "LDDlddfdF"]
middleLayerAdditional = ["D","d"]
yellowCrossStandard = ["FDLdlf","FLDldf"]
yellowCrossAdditional = ["D","d"]
yellowFaceStandard = ["LDlDLDDl"]
yellowFaceAdditional = ["D","d"]
yellowCornersStandard = ["lFlBBLflBBLL", "LLBBLFlBBLfL"]#,"LLUbDbdBuLLfDF" "RRDbUbuBdRRfUF"]
yellowCornersAdditional = ["D","d"]
yellowEdgesStandard = ["RRdBfRRbFdRR", "bUbububUBUBB"]

# This map is used to initialize face colors when the cube is first made
indexMap = {"w" : 0,
            "g" : 1,
            "r" : 2,
            "b" : 3,
            "o" : 4,
            "y" : 5}

# The next three maps are used for peer assignments of each facet (A peer is other colors in the same piece)
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



allMoves = ["u","U","UU","uu",
            "l","L","LL","ll",
            "f","F","FF","ff",
            "r","R","RR","rr",
            "b","B","BB","bb",
            "d","D","DD","dd"]


robotMoves = {
    
    "R":"R",
    "r":"r",
    "RR":"3",
    "rr":"3",
    "L":"L",
    "l":"l",
    "LL":"1",
    "ll":"1",
    "F":"F",
    "f":"f",
    "FF":"2",
    "ff":"2",
    "B":"B",
    "b":"b",
    "BB":"4",
    "bb":"4",
    "U":"T",
    "u":"t",
    "UU":"0",
    "uu":"0",
    "D":"D",
    "d":"d",
    "DD":"5",
    "dd":"5"

}