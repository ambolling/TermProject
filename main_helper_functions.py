import random as rand
from cmu_graphics import *
from person import person

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

def drawConnections(app):
    for key in app.connectedInfections:
        for value in app.connectedInfections[key]:
            # if value not in app.populationInfectedMembers:
                drawLine(key.xVal, key.yVal, value.xVal, value.yVal, opacity = 25, fill = 'grey')

def drawPlayAndPause(app):
    if app.paused:
        drawCircle(app.playButtonX, app.playButtonY, 20, fill = 'white', border = 'black')
        drawCircle(app.pauseButtonX, app.pauseButtonY, 20, fill = 'darkGray', border = 'black')
    else:
        drawCircle(app.playButtonX, app.playButtonY, 20, fill = 'darkGray', border = 'black')
        drawCircle(app.pauseButtonX, app.pauseButtonY, 20, fill = 'white', border = 'black')
    drawPolygon(*app.playButtonPoints, fill = 'black', border = 'black')
    drawRect(app.pauseButtonX-10,app.pauseButtonY-10, 8, 20, fill = 'black')
    drawRect(app.pauseButtonX+2,app.pauseButtonY-10, 8, 20, fill = 'black')

def generateInfectedMemberMiddle(app):
    boardCenterX = (app.populationRightBoundary+app.populationLeftBoundary)//2 
    boardCenterY = (app.populationTopBoundary+app.populationBottomBoundary)//2
    #randomly infect someone in the center of the board
    listOfPeopleInCenter = [] 
    for i in range(app.initialInfectedCount):
        for person in app.populationHealthyMembers:
            xVal = person.xVal
            yVal = person.yVal
            if distance(xVal, boardCenterX, yVal,boardCenterY) < 200:
                person.changeTypeColor('infected','red')
                app.populationHealthyMembers.remove(person)
                app.populationInfectedMembers.append(person)
                listOfPeopleInCenter.append(person)
                break

def generateInfectedMemberRandom(app):
    for i in range(app.initialInfectedCount):
        for person in app.populationHealthyMembers:
            xVal = person.xVal
            yVal = person.yVal
            person.changeTypeColor('infected','red')
            app.populationHealthyMembers.remove(person)
            app.populationInfectedMembers.append(person)
            break

def generateVaccinatedMember(app):
    for i in range(app.initialVaccinatedCount):
        for person in app.populationHealthyMembers:
            xVal = person.xVal
            yVal = person.yVal
            person.changeTypeColor('immune','lightBlue')
            app.populationHealthyMembers.remove(person)
            app.populationImmuneMembers.append(person)
            break

def spreadInfection(app):
    for infectedPerson in app.populationInfectedMembers:
        listOfConnected = []
        if infectedPerson not in app.connectedInfections:
            app.connectedInfections[infectedPerson] = []
        for healthyPerson in app.populationHealthyMembers:
            if distance(infectedPerson.xVal,healthyPerson.xVal,infectedPerson.yVal,healthyPerson.yVal) <= (app.viralRadius+10) and healthyPerson.type == 'healthy':
                listOfConnected.append(healthyPerson)
        numberToInfect = len(listOfConnected)*app.reproductionNumber//100
        for i in range(numberToInfect):
            person = listOfConnected.pop()
            person.changeTypeColor('infected','red')
            app.connectedInfections[infectedPerson].append(person)
    for person in app.populationHealthyMembers:
        if person.type == 'infected':
            app.populationInfectedMembers.append(person)
            app.populationHealthyMembers.remove(person)

def generatePopulation(app):
    for i in range(app.populationSize):
        xVal = rand.randint(app.populationLeftBoundary,app.populationRightBoundary)
        yVal = rand.randint(app.populationTopBoundary,app.populationBottomBoundary)
        newPerson = person(xVal, yVal, 'healthy', 'mediumSeaGreen')
        app.populationHealthyMembers.append(newPerson)
        app.populationAllMembers.append(newPerson)

def isSimulationFinished(app):
    count = 0
    for i in range(len(app.dictChangeOverTimeInfected)-1):
        if app.populationChange[i] == app.populationChange[i+1]:
            return True
    for val in app.connectedInfections:
        if len(app.connectedInfections[val]) == 0:
            count+=1
    if app.day < 2 and count == len(app.connectedInfections):
        return True
    return False    
                  
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

def calculatePersonSize(app):
    personSize = 100/app.populationSize+5
    return personSize

def countHealthy(app):
    count = 0
    for person in app.populationAllMembers:
        if person.type == 'healthy':
            count += 1
    return count

def distance(x1,x2,y1,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5