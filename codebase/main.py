import sys

sys.path.append('./model')
sys.path.append('./detection')

from cube import *


newCube = cube()

face1 = [[
        ["g", "w", "b"],
        ["y", "w", "w"],
        ["y", "g", "o"]
        ],
        [
        ["o", "r", "b"],
        ["r", "g", "b"],
        ["r", "b", "b"]
        ],
        [
        ["r", "y", "y"],
        ["r", "r", "y"],
        ["r", "b", "g"]
        ],
        [
        ["g", "g", "o"],
        ["o", "b", "g"],
        ["w", "w", "o"]
        ],
        [
        ["w", "o", "w"],
        ["o", "o", "g"],
        ["y", "o", "g"]
        ],
        [
        ["w", "y", "r"],
        ["w", "y", "r"],
        ["y", "b", "b"]
        ]]


'''newCube.printCube(newCube.cubeArr)

newCube.scramble(20,newCube.cubeArr)
#newCube.manualScramble(newCube.cubeArr,face1)

newCube.printCube(newCube.cubeArr)


newCube.solveCube()




newCube.printCube(newCube.cubeArr)


print(newCube.solution)
print(len(newCube.solution))
'''

tot = 0
numIters = 1
for i in range(numIters):
    
    newCube.scramble(100,newCube.cubeArr)
    newCube.solveCube()
    
    tot+=len(newCube.solution)
print("Average = ", tot/numIters)


