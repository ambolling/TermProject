from cmu_graphics import *
from person import person

def getPathogenParameters(app):
    drawRect((app.width/20),(app.height/8)+50,(app.width/20)*18,(app.height/4)*3-100, fill = 'white')
    drawLabel(f'Select your parameters for {app.virusName}', app.width/2, (app.height/16)*3+20, size = 20, fill = 'black')
    selectPathogenRadius(app)
    selectPopulationSize(app)
    selectReproductionNumber(app)
    selectStartingNumberOfInfected(app)
    selectStartingNumberOfImmune(app)

def selectPathogenRadius(app):
    drawLabel(f'Select a radius of infection for {app.virusName}: ',app.width/4, app.height/4,size = 16, fill = 'black')
    drawLine((app.width/8)*4, (app.height/4), (app.width/8)*7, app.height/4,fill = 'grey')
    drawLabel(str(app.viralRadius),((app.width/8)*4+(app.width/8)*7)/2, app.height/4+25, size = 20)
    drawCircle(app.radiusSelectorCircleX, app.height/4, 10, fill = 'red')

def selectPopulationSize(app):
    drawLabel('Select a size for your population:',app.width/4, (app.height/8)*3,size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*3, (app.width/8)*7, (app.height/8)*3,fill = 'grey') 
    drawLabel(str(app.populationSize),((app.width/8)*4+(app.width/8)*7)/2, (app.height/8)*3+25, size = 20)
    drawCircle(app.populationSelectorCircleX, (app.height/8)*3, 10, fill = 'red')

def selectReproductionNumber(app):
    drawLabel(f'Transmissability of {app.virusName}:',app.width/4, (app.height/2),size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*4,(app.width/8)*7, (app.height/8)*4,fill = 'grey')
    if app.reproductionNumber != None:
        drawLabel(str(app.reproductionNumber)+'%',((app.width/8)*4+(app.width/8)*7)/2, app.height/2+30, size = 20)
    drawCircle(app.reproductionNumberSelectorCircleX, app.height/2, 10, fill = 'red')

def selectStartingNumberOfInfected(app):
    drawLabel('Number of individuals initially infected:',app.width/4, (app.height/8)*5,size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*5,(app.width/8)*7, (app.height/8)*5,fill = 'grey')
    drawLabel(str(app.initialInfectedCount),((app.width/8)*4+(app.width/8)*7)/2, (app.height/8)*5+25, size = 20)
    drawCircle(app.infectedSelectorCircleX, (app.height/8)*5, 10, fill = 'red')

def selectStartingNumberOfImmune(app):
    drawLabel('Number of individuals initially immune:',app.width/4, (app.height/8)*6,size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*6, (app.width/8)*7, (app.height/8)*6,fill = 'grey')
    drawLabel(str(app.initialVaccinatedCount),((app.width/8)*4+(app.width/8)*7)/2, (app.height/8)*6+25, size = 20)
    drawCircle(app.immuneSelectorCircleX, (app.height/8)*6, 10, fill = 'red')