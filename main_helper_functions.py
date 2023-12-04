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

def drawMainLabels(app):
    drawRect(20, 200, 215, (app.height/8)+10, fill = 'lavender')
    drawLabel('Key',(20+215)/2, 210,size = 20)
    drawCircle(40,250, 10, fill = 'seaGreen')
    drawLabel(' = Healthy', 100, 250, align = 'center', size = 20)
    drawCircle(40,280, 10, fill = 'red')
    drawLabel(' = Infected', 100, 280, align = 'center', size = 20)
    drawCircle(40,310, 10, fill = 'lightBlue', border = 'black')
    drawLabel(' = Immune', 100, 310, align = 'center', size = 20)
    drawLine(app.populationLeftBoundary-10, app.populationTopBoundary-10, app.populationRightBoundary+10, app.populationTopBoundary-10)
    drawLine(app.populationLeftBoundary-10, app.populationTopBoundary-10, app.populationLeftBoundary-10, app.populationBottomBoundary+10)
    drawLine(app.populationLeftBoundary-10, app.populationBottomBoundary+10, app.populationRightBoundary+10, app.populationBottomBoundary+10)
    drawLine(app.populationRightBoundary+10, app.populationBottomBoundary+10, app.populationRightBoundary+10, app.populationTopBoundary-10)
    drawRect(app.populationLeftBoundary-10,app.populationTopBoundary-10, (app.populationRightBoundary+10)-(app.populationLeftBoundary-10),abs((app.populationTopBoundary-10)-(app.populationBottomBoundary+10)), fill = 'white')
    drawLabel("Community Immunity Simulator", app.width/2, app.height/16, size = 50, bold = True, fill = 'white')
    drawLabel('Press r key to reset simulator',(app.width/4)*3+60, (app.height/18)*2, size = 20,bold = True, fill = 'white' )
    drawLabel('Click on a person or hold down and drag to immunize',(app.width/4)*1+60, (app.height/18)*2, size = 23,bold = True, fill = 'black' )
    drawRect(20, 400, 215, 400, fill = 'lavender')
    drawLabel('Size of Population', app.width/8, 425, size = 20)
    drawLabel(app.populationSize, (app.width/8), 450, size = 20)
    drawLabel('Radius of infection', (app.width/8), 500, size = 20)
    drawLabel(app.viralRadius, (app.width/8), 525, size = 20)
    drawLabel('Percentage Immune', (app.width/8), 575, size = 20)
    drawLabel(calculatePercentageImmune(app), (app.width/8), 600, size = 20)
    drawLabel('Percentage Infected', (app.width/8), 650, size = 20)
    drawLabel(calculatePercentageInfected(app), (app.width/8), 675, size = 20)
    drawLabel('Percentage Healthy', (app.width/8), 725, size = 20)
    drawLabel(calculatePercentageHealthy(app), (app.width/8),750, size = 20)

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