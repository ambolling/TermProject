from cmu_graphics import *
import random


def onAppStart(app):
    app.populationHealthyMembers = []
    app.populationInfectedMembers = []
    app.healthyColor = 'green'
    app.populationLeftBoundary = 300
    app.populationRightBoundary = app.width-100
    app.populationTopBoundary = 200
    app.populationBottomBoundary = app.height-200
    app.paused = False
    app.stepsPerSecond = .5
    app.connectedInfections = dict()
    app.viralRadius = 100
    app.viralRadiusOptions = dict()
    app.populationSizes = dict()
    app.populationSize = 100
    app.reproductionNumber = None
    app.reproductionNumbers = dict()

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
    drawMainLabels(app)
    drawPopulation(app)
    drawConnections(app)

def welcome_redrawAll(app):
    drawLabel("Welcome to Community Immunity Simlutor", app.width/2, app.height/8, size = 50)
    getPathogenParameters(app)

def drawMainLabels(app):
    drawLabel("Community Immunity Simulator", app.width/2, app.height/16, size = 50)
    drawLabel('Size of Population', app.width/8, app.width/8, size = 20)
    drawLabel(app.populationSize, (app.width/8), (app.width/8)+25, size = 20)
    drawLabel('Radius of infection', (app.width/8), (app.width/8)*2, size = 20)
    drawLabel(app.viralRadius, (app.width/8), (app.width/8)*2+25, size = 20)


def getPathogenParameters(app):
    selectPathogenContagiousLevel(app)
    selectPopulationSize(app)
    selectReproductionNumber(app)

def selectPathogenContagiousLevel(app):
    drawLabel('Select a radius of infection for your pathogen: ',app.width/4, app.height/4,size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/4), (app.width/8)*7, app.height/4,fill = 'grey')

    drawLabel('40',(app.width/8)*4, app.height/4+25, size = 20)
    drawCircle((app.width/8)*4, app.height/4, 10, fill = 'red')
    app.viralRadiusOptions[40]=[(app.width/8)*4, app.height/4+25]

    drawLabel('100',(app.width/8)*7, app.height/4+25, size = 20)
    drawCircle((app.width/8)*7, app.height/4, 10, fill = 'red')
    app.viralRadiusOptions[100]=[(app.width/8)*4, app.height/4+25]


def selectPopulationSize(app):
    drawLabel('Select a size for your population:',app.width/4, (app.height/8)*3,size = 25, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*3, (app.width/8)*7, (app.height/8)*3,fill = 'grey')
    
    drawLabel('10',(app.width/8)*4, (app.height/8)*3+25, size = 20)
    drawCircle((app.width/8)*4, (app.height/8)*3, 10, fill = 'red')
    app.populationSizes[10] = [(app.width/8)*4, (app.height/8)*3]

    drawLabel('300',(app.width/8)*7, (app.height/8)*3+25, size = 20)
    drawCircle((app.width/8)*7, (app.height/8)*3, 10, fill = 'red')
    app.populationSizes[300] = [(app.width/8)*7, (app.height/8)*3]

def selectReproductionNumber(app):
    drawLabel('Transmissability of your pathogen:',app.width/4, (app.height/2),size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*4,(app.width/8)*7, (app.height/8)*4,fill = 'grey')

    drawLabel('1',app.width/2, app.height/2+30, size = 20)
    drawCircle(app.width/2, app.height/2, 10, fill = 'red')
    app.reproductionNumbers[1] = [app.width/2, app.height/2]

    drawLabel('All',(app.width/8)*7, app.height/2+30, size = 20)
    drawCircle((app.width/8)*7, app.height/2, 10, fill = 'red')
    app.reproductionNumbers[None] = [app.width/2+300, app.height/2]

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
    for value in app.reproductionNumbers:
        if distance(mouseX, app.reproductionNumbers[value][0], mouseY, app.reproductionNumbers[value][1]) <= 10:
            app.reproductionNumber = value

def drawConnections(app):
    for key in app.connectedInfections:
        for value in app.connectedInfections[key]:
            drawLine(key.xVal, key.yVal, value.xVal, value.yVal, opacity = 25, fill = 'grey')

def calculatePersonSize(app):
    personSize = 100/app.populationSize+5
    return personSize

def calculatePercentageImmune(app):
    pass

def calculatePercentageInfected(app):
    pass

def calculatePercentageHealhty(app):
    pass

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
        if distance(xVal, boardCenterX, yVal,boardCenterY) < 200:
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
            if app.reproductionNumber != None and len(app.connectedInfections[infectedPerson]) == app.reproductionNumber:
                break
    for person in app.populationHealthyMembers:
        if person.type == 'infected':
            app.populationInfectedMembers.append(person)
            app.populationHealthyMembers.remove(person)

def distance(x1,x2,y1,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5

def main():
    runAppWithScreens(initialScreen = 'welcome', width = 1000, height = 1000)

main()