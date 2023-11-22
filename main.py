from cmu_graphics import *
import random


def onAppStart(app):
    app.populationHealthyMembers = []
    app.populationInfectedMembers = []
    app.healthyColor = 'green'
    app.populationLeftBoundary = 200
    app.populationRightBoundary = app.width-200
    app.populationTopBoundary = 200
    app.populationBottomBoundary = app.height-200
    app.paused = False
    app.stepsPerSecond = 1
    generatePopulation(app)
    generateInfectedMember(app)

def generatePopulation(app):
    for i in range(100):
        xVal = random.randint(app.populationLeftBoundary,app.populationRightBoundary)
        yVal = random.randint(app.populationTopBoundary,app.populationBottomBoundary)
        newPerson = person(xVal, yVal, 'healthy', 'green')
        app.populationHealthyMembers.append(newPerson)
    

class person():
    def __init__(self, xVal, yVal, type, color):
        self.xVal = xVal
        self.yVal = yVal
        self.type = type
        self.color = color

    def changeTypeColor(self, newType, newColor):
        self.type = newType
        self.color = newColor



def redrawAll(app):
    drawPopulation(app)


def drawPopulation(app):
    for val in app.populationHealthyMembers:
        drawCircle(val.xVal, val.yVal, 10, fill = val.color)
    for val in app.populationInfectedMembers:
        drawCircle(val.xVal, val.yVal, 10, fill = val.color)

def generateInfectedMember(app):
    boardCenterX = (app.populationRightBoundary+app.populationLeftBoundary)//2 
    boardCenterY = (app.populationTopBoundary+app.populationBottomBoundary)//2
    #randomly infect someone in the center of the board 
    for person in app.populationHealthyMembers:
        xVal = person.xVal
        yVal = person.yVal
        if distance(xVal, boardCenterX, yVal,boardCenterY) < 100:
            person.changeTypeColor('infected','red')
            app.populationHealthyMembers.remove(person)
            app.populationInfectedMembers.append(person)
            break
    

def onKeyPress(app, key):
    if key == 'g':
        spreadInfection(app)

def spreadInfection(app):
    for infectedPerson in app.populationInfectedMembers:
        for healthyPerson in app.populationHealthyMembers:
            if distance(infectedPerson.xVal,healthyPerson.xVal,infectedPerson.yVal,healthyPerson.yVal) <= (100+10):
                healthyPerson.changeTypeColor('infected','red')
    for person in app.populationHealthyMembers:
        if person.type == 'infected':
            app.populationInfectedMembers.append(person)
            app.populationHealthyMembers.remove(person)




def distance(x1,x2,y1,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5

def main():
    runApp(width = 1000, height = 1000)

main()