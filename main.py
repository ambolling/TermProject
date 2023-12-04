from cmu_graphics import *
from PIL import Image
from main_helper_functions import *
from parameters_helper_functions import *
from finished_helper_functions import *
from person import *

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
    app.viralRadius = 10
    app.populationSize = 10
    app.initialInfectedCount = 1
    app.reproductionNumber = 10
    app.finished = False
    app.populationSelected = False
    app.populationSelectorCircleX = (app.width/8)*4
    app.radiusSelected = False
    app.radiusSelectorCircleX = (app.width/8)*4
    app.reproductionNumberSelected = False
    app.reproductionNumberSelectorCircleX = app.width/2
    app.infectedSelected = False
    app.infectedSelectorCircleX = app.width/2
    app.dictChangeOverTimeInfected = dict()
    app.dictChangeOverTimeHealthy = dict()
    app.dictChangeOverTimeImmune = dict()
    app.day = 1
    app.populationChange = []
    app.initialVaccinatedCount = 0
    app.immuneSelectorCircleX = app.width/2
    app.immuneSelected = False

    #Image Citation: Image by <a href="https://pixabay.com/users/thedigitalartist-202249/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4922384">Pete Linforth</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4922384">Pixabay</a>
    app.vb = 'virusbackground.jpg'

def main_redrawAll(app):
    if len(app.populationInfectedMembers) == 0:
        generateInfectedMemberMiddle(app)
        generateVaccinatedMember(app)
        if len(app.populationInfectedMembers) == 0:
            generateInfectedMemberRandom(app)
    drawMainLabels(app)
    drawPlayAndPause(app)
    if app.finished == False:
        drawPopulation(app)
        drawConnections(app)
    else:
        drawPopulation(app)
        drawConnections(app)
        setActiveScreen('finished')

def finished_redrawAll(app):
    drawBackground(app)
    drawRect(150,250,700,450,fill = 'white')
    drawGraph(app)
    drawLabel('Your simulation is complete!',app.width/2,100, size = 50, fill = 'white', bold = True)
    drawLabel(f'Your simulation lasted {len(app.dictChangeOverTimeInfected)} days',app.width/2,200, size = 25, fill = 'white', bold = True)

def drawMainLabels(app):
    drawBackground(app)
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

def main_onStep(app):
    if not app.paused:
        countInfected = 0
        countHealthy = 0
        for person in app.populationAllMembers:
            if person.type == 'infected':
                countInfected +=1
        for person in app.populationAllMembers:
            if person.type == 'healthy':
                countHealthy +=1
        app.populationChange.append(countInfected)
        app.dictChangeOverTimeInfected[app.day] = countInfected
        app.dictChangeOverTimeHealthy[app.day] = countHealthy
        app.day += 1

    if not app.paused and not isSimulationFinished(app):
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

def welcome_redrawAll(app):
    drawBackground(app)
    # drawLabel("Welcome to", app.width/2, app.height/8, size = 50, align = 'center', fill = 'white')
    drawLabel('Community',app.width/2, app.height/4, size = 110, bold = True, fill = 'lightGreen')
    drawLabel('Community',app.width/2.05, app.height/4, size = 110, bold = True, fill = 'seaGreen',border = 'black')
    drawLabel('Immunity',app.width/2, (app.height/8)*3, size = 110,bold = True, fill = 'lavender')
    drawLabel('Immunity',app.width/2.05, (app.height/8.1)*3, size = 110,bold = True, fill = 'indigo',border = 'black')
    drawLabel('Simulator',app.width/2, (app.height/8)*4, size = 110,bold = True, fill = 'lightGreen')
    drawLabel('Simulator',app.width/2.05, (app.height/8.1)*4, size = 110,bold = True, fill = 'seaGreen', border = 'black')
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
    if distance(mouseX, app.infectedSelectorCircleX, mouseY, (app.height/8)*5) <= 10:
        app.infectedSelected = True
    if distance(mouseX, app.immuneSelectorCircleX, mouseY, (app.height/8)*6) <= 10:
        app.immuneSelected = True
    
def parameters_onMouseRelease(app, mouseX, mouseY):
    app.populationSelected = False
    app.radiusSelected = False
    app.reproductionNumberSelected = False
    app.infectedSelected = False
    app.immuneSelected = False

def parameters_onMouseDrag(app, mouseX, mouseY):
    sliderSelection(app, mouseX, mouseY)

def distance(x1,x2,y1,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5

def main():
    runAppWithScreens(initialScreen = 'welcome', width = 1000, height = 1000)

main()