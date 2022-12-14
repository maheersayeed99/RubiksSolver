# RubiksSolver

This program is able to take in the colors of a scrambled Rubik's Cube, and return a series of moves that will solve it. OpenCV is used to detect the colors. Once the scrambled cube is scanned into the program, it is fed into the solving algorithm which uses graph generation along with Dijkstra shortest path-finding to return a valid solution. Ideally, this program will be paired with a robot capable of solving the real cube using the generated algorithm. To learn more about the project, visit https://maheersayeed.wordpress.com/

## Run
To run the project, clone the library and make sure you are in the folder containing main.py. Running main.py will begin the application

In order to run this program, you need to download the OpenCV library 

## Use
The program uses a webcam. Once the program is run, you will see bounding lines forming a square. Hold the cube in the middle of the square.
In order to orient the cube properly, use the colors of the bounding box walls. If the wall color is blue, that means the cube side with the blue ccenter will face that direction. 
If the cube is held correctly for three seconds, the program will automatically detects the colors of the face.
Rotate through all six faces correctly to scan the whole cube before pressing m to solve

![Depth First Search with 125 X 250 Maze](https://github.com/maheersayeed99/RubiksSolver/blob/main/pictures/Main%20Page.png)  

The moves that will solve the cube are printed on the terminal. Lower case letters mean a counter clocwise rotation and upper case letters mean a clockwise rotation.  

U/u = top   = White  
L/l = left  = Green  
F/f = front = Red  
R/r = right = Blue  
B/b = back  = Orange  
D/d = down  = Yellow


## Controls

`R` moves to the next cube face  
`L` moves to the previous cube state  
`Z` lowers contour detections sensitivity  
`X` increases contour detection sensitivity  
`M` solves the cube and returns the solution at the terminal, only if all 6 faces are scanned properly  
`N` changes the color thresholds between daytime and nighttime tunings  
`S` Detects current colors (use if auto detect malfunctions)  
