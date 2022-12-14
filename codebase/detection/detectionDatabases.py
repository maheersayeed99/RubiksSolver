
# Map used to get bgr values of color strings
bgrMap = {
    "w" : (255,255,255),
    "g" : (50,205,50),
    "r" : (46,46,255),
    "b" : (255,105,65),
    "o" : (0,140,255),
    "y" : (0,215,255),
    "k" : (0,0,0)
}

# Map used to determine the color of each face
indexArr = ["w","g","r","b","o","y"]

# Map used to color the orientation lines
orientationLineChanges = ["ogrb","woyr","wgyb","wryo","wbyg","rgob"]

# HSV upper and lower thresholds
# Daytime

daytimeHSV = [
    [[0,0,168],[172,111,255]],
    [[36,0,0], [86,255,255]],
    [[160,100,20], [179,255,255]],
    [[96,62,62], [130,255,255]],
    [[ 4,100,100], [8,255,255]],
    [[15,0,0], [21,255,255]]
]

# Nighttime

nighttimeHSV = [
    [[0,0,168],[172,111,255]], 
    [[36,50,0], [86,255,255]],
    [[0,50,50], [10,255,255]],
    [[96,62,62], [130,255,255]],    # works same as before
    [[ 5,100,100], [17,255,255]],
    [[15,50,0], [36,255,255]]        # upper changed
]