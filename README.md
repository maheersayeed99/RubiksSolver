# RubiksSolver

This program is able to take in the colors of a scrambled Rubik's Cube, and return a series of moves that will solve it. OpenCV is used to detect the colors. Once the scrambled cube is scanned into the program, it is fed into the solving algorithm which uses graph generation along with Dijkstra shortest path-finding to return a valid solution. Ideally, this program will be paired with a robot capable of solving the real cube using the generated algorithm. To learn more about the project, visit https://www.maheersayeed.wordpress.com


To run the project, clone the library and make sure you are in the folder containing main.py. Running main.py will begin the application

In order to run this program, you need to download the OpenCV library 


Controls

pressing r moves to the next cube face
pressing l moves to the previous cube state
pressing z lowers contour detections sensitivity
pressing x increases contour detection sensitivity
pressing m solves the cube and returns the solution at the terminal, only if all 6 faces are scanned properly
pressing s changes the color thresholds between daytime and nighttime tunings
