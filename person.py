from cmu_graphics import *

class person():
    def __init__(self, xVal, yVal, type, color):
        self.xVal = xVal
        self.yVal = yVal
        self.type = type
        self.color = color

    def changeTypeColor(self, newType, newColor):
        self.type = newType
        self.color = newColor
