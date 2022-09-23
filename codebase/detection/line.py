import cv2

class line():
    def __init__(self, xi, yi, deltax, deltay, thickness, color) -> None:

        self.xi = xi
        self.deltax = deltax
        self.yi = yi
        self.deltay = deltay
        self.thickness = thickness
        
        self.blue = color[0]
        self.green = color[1]
        self.red = color[2]
        

    
    def changeColor(self, color):
        
        self.blue = color[0]
        self.green = color[1]
        self.red = color[2]


    def draw(self, canvas):
        cv2.line(canvas,(self.xi,self.yi),(self.xi+self.deltax, self.yi+self.deltay), (self.blue,self.green, self.red), self.thickness)





