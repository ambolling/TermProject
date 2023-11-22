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
    app.stepsPerSecond = .5
    app.connectedInfections = dict()
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

def main_redrawAll(app):
    drawPopulation(app)
    drawConnections(app)

def welcome_redrawAll(app):
    drawLabel("Welcome to Community Immunity", app.width/2, app.height/4, size = 50)
    getPathogenParameters(app)


def drawConnections(app):
    for key in app.connectedInfections:
        for value in app.connectedInfections[key]:
            drawLine(key.xVal, key.yVal, value.xVal, value.yVal, opacity = 25, fill = 'grey')



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
    
def main_onStep(app):
    if not app.paused:
        spreadInfection(app)
        
def main_onMousePress(app, mouseX, mouseY):
    for person in app.populationHealthyMembers:
        if distance(person.xVal, mouseX, person.yVal, mouseY) <= 10:
            person.changeTypeColor('immune','lightBlue')

def main_onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused

def welcome_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('main')

def spreadInfection(app):
    for infectedPerson in app.populationInfectedMembers:
        app.connectedInfections[infectedPerson] = []
        for healthyPerson in app.populationHealthyMembers:
            if distance(infectedPerson.xVal,healthyPerson.xVal,infectedPerson.yVal,healthyPerson.yVal) <= (100+10) and healthyPerson.type != 'immune':
                healthyPerson.changeTypeColor('infected','red')
                app.connectedInfections[infectedPerson].append(healthyPerson)
    for person in app.populationHealthyMembers:
        if person.type == 'infected':
            app.populationInfectedMembers.append(person)
            app.populationHealthyMembers.remove(person)




def distance(x1,x2,y1,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5

def main():
    runAppWithScreens(initialScreen = 'welcome', width = 1000, height = 1000)

main()