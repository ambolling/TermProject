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
    app.viralRadius = 100
    app.viralRadiusOptions = dict()
    app.populationSizes = dict()
    app.populationSize = 100
    # app.personSize = 10


def generatePopulation(app):
    for i in range(app.populationSize):
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
    if len(app.populationInfectedMembers) == 0:
        generateInfectedMember(app)
    drawPopulation(app)
    drawConnections(app)

def welcome_redrawAll(app):
    drawLabel("Welcome to Community Immunity", app.width/2, app.height/4, size = 50)
    getPathogenParameters(app)
    selectPopulationSize(app)


def getPathogenParameters(app):
    selectPathogenContagiousLevel(app)

def selectPathogenContagiousLevel(app):
    drawLabel('Select a radius for infection:',app.width/4, app.height/3,size = 25, fill = 'pink')
    drawLine(app.width/2, app.height/3, app.width/2+300, app.height/3,fill = 'grey')

    drawLabel('40',app.width/2, app.height/3+30, size = 20)
    drawCircle(app.width/2, app.height/3, 10, fill = 'red')
    app.viralRadiusOptions[40]=[app.width/2, app.height/3]

    drawLabel('100',app.width/2+300, app.height/3+30, size = 20)
    drawCircle(app.width/2+300, app.height/3, 10, fill = 'red')
    app.viralRadiusOptions[100]=[app.width/2+300, app.height/3]


def selectPopulationSize(app):
    drawLabel('Select a size for your population:',app.width/4, app.height/2,size = 25, fill = 'pink')
    drawLine(app.width/2, app.height/2, app.width/2+300, app.height/2,fill = 'grey')
    
    drawLabel('10',app.width/2, app.height/2+30, size = 20)
    drawCircle(app.width/2, app.height/2, 10, fill = 'red')
    app.populationSizes[10] = [app.width/2, app.height/2]

    drawLabel('300',app.width/2+300, app.height/2+30, size = 20)
    drawCircle(app.width/2+300, app.height/2, 10, fill = 'red')
    app.populationSizes[300] = [app.width/2+300, app.height/2]


def welcome_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('main')
    
def welcome_onMousePress(app, mouseX, mouseY):
    for value in app.populationSizes:
        if distance(mouseX,app.populationSizes[value][0], mouseY, app.populationSizes[value][1]) <= 10:
            print(app.populationSize)
            app.populationSize = value
    for value in app.viralRadiusOptions:
        if distance(mouseX, app.viralRadiusOptions[value][0], mouseY, app.viralRadiusOptions[value][1]) <= 10:
            app.viralRadius = value

def drawConnections(app):
    for key in app.connectedInfections:
        for value in app.connectedInfections[key]:
            drawLine(key.xVal, key.yVal, value.xVal, value.yVal, opacity = 25, fill = 'grey')

def calculatePersonSize(app):
    personSize = 100/app.populationSize+5
    return personSize

def drawPopulation(app):
    if len(app.populationHealthyMembers) == 0:
        generatePopulation(app)
    else:
        personSize = calculatePersonSize(app)
        for val in app.populationHealthyMembers:
            drawCircle(val.xVal, val.yVal, personSize, fill = val.color)
        for val in app.populationInfectedMembers:
            drawCircle(val.xVal, val.yVal, personSize, fill = val.color)


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


def spreadInfection(app):
    for infectedPerson in app.populationInfectedMembers:
        app.connectedInfections[infectedPerson] = []
        for healthyPerson in app.populationHealthyMembers:
            if distance(infectedPerson.xVal,healthyPerson.xVal,infectedPerson.yVal,healthyPerson.yVal) <= (app.viralRadius+10) and healthyPerson.type != 'immune':
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