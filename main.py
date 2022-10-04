from os import lseek
import sys

print(sys.path)





sys.path.append('/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages')
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

