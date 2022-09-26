import sys

sys.path.append('./codebase/model')
sys.path.append('./codebase/detection')

from cube import *
from application import *


newCube = cube()
myApp = app(newCube)

while not myApp.terminate():
    myApp.process()
    myApp.run()
    myApp.draw()

