from cmu_graphics import *
import random
from PIL import Image

def onAppStart(app):
    resetApp(app)

def resetApp(app):
    app.populationAllMembers = []
    app.populationHealthyMembers = []
    app.populationInfectedMembers = []
    app.populationImmuneMembers = []
    app.healthyColor = 'mediumSeaGreen'
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
    app.populationSize = 10
    app.reproductionNumber = None
    app.finished = False
    app.populationSelected = False
    app.populationSelectorCircleX = (app.width/8)*4
    app.radiusSelected = False
    app.radiusSelectorCircleX = (app.width/8)*4
    app.reproductionNumberSelected = False
    app.reproductionNumberSelectorCircleX = app.width/2

    #Image Citation: Image by <a href="https://pixabay.com/users/thedigitalartist-202249/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4922384">Pete Linforth</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4922384">Pixabay</a>
    app.vb = 'virusbackground.jpg'


def generatePopulation(app):
    for i in range(app.populationSize):
        xVal = random.randint(app.populationLeftBoundary,app.populationRightBoundary)
        yVal = random.randint(app.populationTopBoundary,app.populationBottomBoundary)
        newPerson = person(xVal, yVal, 'healthy', 'mediumSeaGreen')
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
    drawBackground(app)
    drawRect(20, app.height/8-10, 215, (app.height/8)*6, fill = 'lavender')
    drawLine(app.populationLeftBoundary-10, app.populationTopBoundary-10, app.populationRightBoundary+10, app.populationTopBoundary-10)
    drawLine(app.populationLeftBoundary-10, app.populationTopBoundary-10, app.populationLeftBoundary-10, app.populationBottomBoundary+10)
    drawLine(app.populationLeftBoundary-10, app.populationBottomBoundary+10, app.populationRightBoundary+10, app.populationBottomBoundary+10)
    drawLine(app.populationRightBoundary+10, app.populationBottomBoundary+10, app.populationRightBoundary+10, app.populationTopBoundary-10)
    drawRect(app.populationLeftBoundary-10,app.populationTopBoundary-10, (app.populationRightBoundary+10)-(app.populationLeftBoundary-10),abs((app.populationTopBoundary-10)-(app.populationBottomBoundary+10)), fill = 'white')
    drawLabel("Community Immunity Simulator", app.width/2, app.height/16, size = 50, bold = True, fill = 'white')
    drawLabel('Press r key to reset simulator',app.width/2, (app.height/18)*2, size = 18,bold = True, fill = 'white' )
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
    drawBackground(app)
    # drawLabel("Welcome to", app.width/2, app.height/8, size = 50, align = 'center', fill = 'white')
    drawLabel('Community',app.width/2, app.height/4, size = 90, font = 'grenze', bold = True, fill = 'lightGreen')
    drawLabel('Community',app.width/1.95, app.height/4.1, size = 90,bold = True, fill = 'seaGreen',border = 'black')
    drawLabel('Immunity',app.width/2, (app.height/8)*3, size = 100,bold = True, fill = 'lavender')
    drawLabel('Immunity',app.width/2.05, (app.height/8.1)*3, size = 100,bold = True, fill = 'indigo',border = 'black')
    drawLabel('Simulator',app.width/2, (app.height/8)*4, size = 100,bold = True, fill = 'lightGreen')
    drawLabel('Simulator',app.width/1.95, (app.height/7.9)*4, size = 100,bold = True, fill = 'seaGreen', border = 'black')
    drawLabel('Press the space bar to begin the simulation', app.width/2, (app.height/16)*14, size = 30, fill = 'white', bold = True)

    
def drawBackground(app):
    imageWidth, imageHeight = getImageSize(app.vb)
    drawImage(app.vb, app.width/2, app.height/2, align='center',
              width=imageWidth, height=imageHeight)

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

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
    drawRect((app.width/20),(app.height/8)+50,(app.width/20)*18,(app.height/4)*3, fill = 'white')
    selectPathogenRadius(app)
    selectPopulationSize(app)
    selectReproductionNumber(app)
    selectStartingNumberOfInfected(app)

def selectPathogenRadius(app):
    drawLabel('Select a radius of infection for your pathogen: ',app.width/4, app.height/4,size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/4), (app.width/8)*7, app.height/4,fill = 'grey')

    drawLabel(str(app.viralRadius),((app.width/8)*4+(app.width/8)*7)/2, app.height/4+25, size = 20)
    drawCircle(app.radiusSelectorCircleX, app.height/4, 10, fill = 'red')
    # app.viralRadiusOptions[40]=[(app.width/8)*4, app.height/4+25]

    # drawLabel('100',(app.width/8)*7, app.height/4+25, size = 20)
    # drawCircle((app.width/8)*7, app.height/4, 10, fill = 'red')
    # app.viralRadiusOptions[100]=[(app.width/8)*4, app.height/4+25]


def selectPopulationSize(app):
    drawLabel('Select a size for your population:',app.width/4, (app.height/8)*3,size = 25, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*3, (app.width/8)*7, (app.height/8)*3,fill = 'grey')
    
    drawLabel(str(app.populationSize),((app.width/8)*4+(app.width/8)*7)/2, (app.height/8)*3+25, size = 20)
    drawCircle(app.populationSelectorCircleX, (app.height/8)*3, 10, fill = 'red')

def selectReproductionNumber(app):
    drawLabel('Transmissability of your pathogen:',app.width/4, (app.height/2),size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*4,(app.width/8)*7, (app.height/8)*4,fill = 'grey')
    if app.reproductionNumber != None:
        drawLabel(str(app.reproductionNumber)+'%',((app.width/8)*4+(app.width/8)*7)/2, app.height/2+30, size = 20)
    drawCircle(app.reproductionNumberSelectorCircleX, app.height/2, 10, fill = 'red')


def selectStartingNumberOfInfected(app):
    #define parameter or number of infected individuals spawned in beginning
    drawLabel('Number of individuals initially infected:',app.width/4, (app.height/8)*5,size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*5,(app.width/8)*7, (app.height/8)*5,fill = 'grey')

def parameters_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('main')

def parameters_redrawAll(app):
    drawBackground(app)
    drawLabel("Welcome to Community Immunity Simlutor", app.width/2, app.height/8, size = 45, fill = 'white', bold= True)
    drawLabel('Select your parameters', app.width/2, (app.height/16)*3, size = 20, fill = 'white', bold = True)
    drawLabel('Press the space bar to begin the simulation', app.width/2, (app.height/16)*14, size = 30, fill = 'white', bold = True)
    getPathogenParameters(app)
    
def parameters_onMousePress(app, mouseX, mouseY):
    if distance(mouseX,app.populationSelectorCircleX, mouseY, (app.height/8)*3) <= 10:
        app.populationSelected = True
    if distance(mouseX,app.radiusSelectorCircleX, mouseY, app.height/4) <= 10:
        app.radiusSelected = True
    if distance(mouseX,app.reproductionNumberSelectorCircleX, mouseY, app.height/2) <= 10:
        app.reproductionNumberSelected = True

def parameters_onMouseRelease(app, mouseX, mouseY):
    app.populationSelected = False
    app.radiusSelected = False
    app.reproductionNumberSelected = False


def parameters_onMouseDrag(app, mouseX, mouseY):
    if app.populationSelected:
        if ((app.width/8)*4) <= mouseX and mouseX <= ((app.height/8)*7+10):
            distanceDotFromStart = distance(mouseX,((app.width/8)*4),mouseY, (app.height/8)*3)
            if distanceDotFromStart <= 20:
                app.populationSize =10
            elif distanceDotFromStart >= 20 and distanceDotFromStart <=40:
                app.populationSize =20
            elif distanceDotFromStart >= 40 and distanceDotFromStart <=80:
                app.populationSize =40
            elif distanceDotFromStart >= 80 and distanceDotFromStart <=100:
                app.populationSize =80
            elif distanceDotFromStart >= 100 and distanceDotFromStart <=120:
                app.populationSize =100
            elif distanceDotFromStart >= 120 and distanceDotFromStart <=140:
                app.populationSize =120
            elif distanceDotFromStart >= 140 and distanceDotFromStart <=180:
                app.populationSize =140
            elif distanceDotFromStart >= 180 and distanceDotFromStart <=200:
                app.populationSize =160
            elif distanceDotFromStart >= 200 and distanceDotFromStart <=220:
                app.populationSize =180
            elif distanceDotFromStart >= 220 and distanceDotFromStart <=240:
                app.populationSize =200
            elif distanceDotFromStart >= 240 and distanceDotFromStart <=280:
                app.populationSize =220
            elif distanceDotFromStart >= 280 and distanceDotFromStart <=300:
                app.populationSize =240
            elif distanceDotFromStart >= 300 and distanceDotFromStart <=320:
                app.populationSize =280
            elif distanceDotFromStart >= 320 and distanceDotFromStart <=340:
                app.populationSize =300
            elif distanceDotFromStart >= 340 and distanceDotFromStart <=380:
                app.populationSize =320
            app.populationSelectorCircleX = mouseX
    if app.radiusSelected:
        if ((app.width/8)*4) <= mouseX and mouseX <= (app.width/8)*7:
            distanceDotFromStart = distance(mouseX,((app.width/8)*4),mouseY, (app.height/4+25))
            if distanceDotFromStart <= 50:
                app.viralRadius = 10
            elif distanceDotFromStart >= 50 and distanceDotFromStart <=100:
                app.viralRadius =20
            elif distanceDotFromStart >= 150 and distanceDotFromStart <=200:
                app.viralRadius =40
            elif distanceDotFromStart >= 250 and distanceDotFromStart <=300:
                app.viralRadius =80
            elif distanceDotFromStart >= 350 and distanceDotFromStart <=400:
                app.viralRadius =100
            app.radiusSelectorCircleX = mouseX
    if app.reproductionNumberSelected:
        if ((app.width/8)*4) <= mouseX and mouseX <= (app.width/8)*7:
            distanceDotFromStart = distance(mouseX,app.width/2,mouseY, app.height/2)
            if distanceDotFromStart <= 50:
                app.reproductionNumber = 10
            elif distanceDotFromStart >= 50 and distanceDotFromStart <=100:
                app.reproductionNumber =20
            elif distanceDotFromStart >= 150 and distanceDotFromStart <=200:
                app.reproductionNumber =40
            elif distanceDotFromStart >= 250 and distanceDotFromStart <=300:
                app.reproductionNumber =80
            elif distanceDotFromStart >= 350 and distanceDotFromStart <=400:
                app.reproductionNumber =100
            app.reproductionNumberSelectorCircleX = mouseX
            

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