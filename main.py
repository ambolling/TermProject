from cmu_graphics import *
import random
import math

def onAppStart(app):
    resetApp(app)

def resetApp(app):
    app.populationAllMembers = []
    app.populationHealthyMembers = []
    app.populationInfectedMembers = []
    app.populationImmuneMembers = []
    app.healthyColor = 'green'
    app.populationLeftBoundary = 300
    app.populationRightBoundary = app.width-100
    app.populationTopBoundary = 200
    app.populationBottomBoundary = app.height-200
    app.paused = False
    app.pauseButtonX = (app.populationLeftBoundary+app.populationRightBoundary)/2+30
    app.pauseButtonY = app.populationTopBoundary-50
    app.playButtonX = (app.populationLeftBoundary+app.populationRightBoundary)/2-30
    app.playButtonY = app.populationTopBoundary-50
    app.playButtonPoints = [(app.populationLeftBoundary+app.populationRightBoundary)/2-40,app.populationTopBoundary-60,
                            (app.populationLeftBoundary+app.populationRightBoundary)/2-40,app.populationTopBoundary-40,
                            (app.populationLeftBoundary+app.populationRightBoundary)/2-15,app.populationTopBoundary-50]
    app.stepsPerSecond = .5
    app.connectedInfections = dict()
    app.viralRadius = 100
    app.viralRadiusOptions = dict()
    app.populationSizes = dict()
    app.populationSize = 100
    app.reproductionNumber = None
    app.reproductionNumbers = dict()
    app.finished = False

def generatePopulation(app):
    for i in range(app.populationSize):
        xVal = random.randint(app.populationLeftBoundary,app.populationRightBoundary)
        yVal = random.randint(app.populationTopBoundary,app.populationBottomBoundary)
        newPerson = person(xVal, yVal, 'healthy', 'green')
        app.populationHealthyMembers.append(newPerson)
        app.populationAllMembers.append(newPerson)

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
    drawPlayAndPause(app)
    if app.finished == False:
        drawPopulation(app)
        drawConnections(app)
    else:
        drawPopulation(app)
        drawConnections(app)
        drawFinishedLabels(app)

def drawMainLabels(app):
    drawLabel("Community Immunity Simulator", app.width/2, app.height/16, size = 50)
    drawLabel('Press r key to reset simulator',app.width/2, (app.height/18)*2, size = 18 )
    drawLabel('Size of Population', app.width/8, app.width/8, size = 20)
    drawLabel(app.populationSize, (app.width/8), (app.width/8)+25, size = 20)
    drawLabel('Radius of infection', (app.width/8), (app.width/8)*2, size = 20)
    drawLabel(app.viralRadius, (app.width/8), (app.width/8)*2+25, size = 20)
    drawLabel('Percentage Immune', (app.width/8), (app.width/8)*3, size = 20)
    drawLabel(calculatePercentageImmune(app), (app.width/8), (app.width/8)*3+25, size = 20)
    drawLabel('Percentage Infected', (app.width/8), (app.width/8)*4, size = 20)
    drawLabel(calculatePercentageInfected(app), (app.width/8), (app.width/8)*4+25, size = 20)
    drawLabel('Percentage Healthy', (app.width/8), (app.width/8)*5, size = 20)
    drawLabel(calculatePercentageHealthy(app), (app.width/8), (app.width/8)*5+25, size = 20)

def main_onStep(app):
    if not app.paused:
        spreadInfection(app)
    if isSimulationFinished(app):
        app.paused = True
        app.finished = True

def main_onMousePress(app, mouseX, mouseY):
    for person in app.populationHealthyMembers:
        if distance(person.xVal, mouseX, person.yVal, mouseY) <= 10:
            person.changeTypeColor('immune','lightBlue')
            app.populationHealthyMembers.remove(person)
            app.populationImmuneMembers.append(person)
    if distance(mouseX, app.pauseButtonX, mouseY, app.pauseButtonY) <= 20:
        app.paused = True
    if distance(mouseX, app.playButtonX, mouseY, app.playButtonY) <= 20:
        app.paused = False 

def main_onMouseDrag(app, mouseX, mouseY):
    for person in app.populationHealthyMembers:
        if distance(person.xVal, mouseX, person.yVal, mouseY) <= 10:
            person.changeTypeColor('immune','lightBlue')
            app.populationHealthyMembers.remove(person)
            app.populationImmuneMembers.append(person)

def main_onKeyPress(app, key):
    if key == 'r':
        resetApp(app)
        setActiveScreen('parameters')

def isSimulationFinished(app):
    if noHealthyInRange(app):
        app.finished = True
        return True
    if len(app.populationInfectedMembers) > 1:
        count = 0
        if countHealthy(app) == 0:
            app.finished = True
            return True
        for value in app.connectedInfections:
            if len(app.connectedInfections[value]) == 0:
                count += 1
        if count == len(app.connectedInfections):
            app.finished = True
            return True 
      
def noHealthyInRange(app):
    if len(app.populationInfectedMembers) != 0:
        for infectedPerson in app.populationAllMembers:
            listOfNeighbors = []
            if infectedPerson.type == 'infected':
                for value in app.populationAllMembers:
                    if distance(infectedPerson.xVal,value.xVal,infectedPerson.yVal,value.yVal) <= (app.viralRadius+10):
                        listOfNeighbors.append(value)
            for value in listOfNeighbors:
                if value.type == 'healthy':
                    return False
        return True
    else:
        return False    
                    
def welcome_redrawAll(app):
    drawLabel("Welcome to Community Immunity Simlutor", app.width/2, app.height/8, size = 50)

def welcome_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('parameters')

def drawFinishedLabels(app):
    drawLabel('DONE', app.width/2, app.width/2, size = 100)
    
def drawPlayAndPause(app):
    drawCircle(app.playButtonX, app.playButtonY, 20, fill = 'white', border = 'black')
    drawPolygon(*app.playButtonPoints, fill = 'black', border = 'black')
    drawCircle(app.pauseButtonX, app.pauseButtonY, 20, fill = 'white', border = 'black')
    drawRect(app.pauseButtonX-10,app.pauseButtonY-10, 8, 20, fill = 'black')
    drawRect(app.pauseButtonX+2,app.pauseButtonY-10, 8, 20, fill = 'black')

def getPathogenParameters(app):
    selectPathogenContagiousLevel(app)
    selectPopulationSize(app)
    selectReproductionNumber(app)
    selectStartingNumberOfInfected(app)

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

def selectStartingNumberOfInfected(app):
    #define parameter or number of infected individuals spawned in beginning
    drawLabel('Number of individuals initially infected:',app.width/4, (app.height/8)*5,size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*5,(app.width/8)*7, (app.height/8)*5,fill = 'grey')

def parameters_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('main')

def parameters_redrawAll(app):
    drawLabel("Welcome to Community Immunity Simlutor", app.width/2, app.height/8, size = 50)
    drawLabel('Select your parameters', app.width/2, (app.height/16)*3, size = 20)
    drawLabel('Press the space bar to begin the simulation', app.width/2, (app.height/16)*14, size = 20)
    getPathogenParameters(app)
    
def parameters_onMousePress(app, mouseX, mouseY):
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
            # if value not in app.populationInfectedMembers:
                drawLine(key.xVal, key.yVal, value.xVal, value.yVal, opacity = 25, fill = 'grey')
                 
def calculatePersonSize(app):
    personSize = 100/app.populationSize+5
    return personSize

def calculatePercentageImmune(app):
    totalImmune = 0
    for person in app.populationAllMembers:
        if person.type == 'immune':
            totalImmune += 1
    decimalImmune = (totalImmune/app.populationSize)
    percentage = rounded((decimalImmune)*100)
    if percentage < 1:
        return '<1%'
    else:
        return f'{percentage}%'

def calculatePercentageInfected(app):
    totalInfected = 0
    for person in app.populationAllMembers:
        if person.type == 'infected':
            totalInfected +=1 
    decimalInfected = (totalInfected/app.populationSize)
    percentage = rounded((decimalInfected)*100)
    if percentage < 1:
        return '<1%'
    else:
        return f'{percentage}%'

def calculatePercentageHealthy(app):
    totalHealthy = 0
    for person in app.populationAllMembers:
        if person.type == 'healthy':
            totalHealthy += 1
    decimalHealthy = (totalHealthy/app.populationSize)
    percentage = rounded((decimalHealthy)*100)
    if percentage < 1:
        return '<1%'
    else:
        return f'{percentage}%'

def countHealthy(app):
    count = 0
    for person in app.populationAllMembers:
        if person.type == 'healthy':
            count += 1
    return count

def drawPopulation(app):
    if len(app.populationHealthyMembers) == 0:
        generatePopulation(app)
    else:
        personSize = calculatePersonSize(app)
        for val in app.populationHealthyMembers:
            drawCircle(val.xVal, val.yVal, personSize, fill = val.color)
        for val in app.populationInfectedMembers:
            drawCircle(val.xVal, val.yVal, personSize, fill = val.color)
        for val in app.populationImmuneMembers:
            drawCircle(val.xVal, val.yVal, personSize, fill = val.color, border = 'black')

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
    
def spreadInfection(app):
    for infectedPerson in app.populationInfectedMembers:
        if infectedPerson not in app.connectedInfections:
            app.connectedInfections[infectedPerson] = []
        for healthyPerson in app.populationHealthyMembers:
            if distance(infectedPerson.xVal,healthyPerson.xVal,infectedPerson.yVal,healthyPerson.yVal) <= (app.viralRadius+10) and healthyPerson.type == 'healthy':
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