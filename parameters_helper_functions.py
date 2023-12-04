from cmu_graphics import *
from person import person

def getPathogenParameters(app):
    drawRect((app.width/20),(app.height/8)+50,(app.width/20)*18,(app.height/4)*3-100, fill = 'white')
    selectPathogenRadius(app)
    selectPopulationSize(app)
    selectReproductionNumber(app)
    selectStartingNumberOfInfected(app)
    selectStartingNumberOfImmune(app)

def selectPathogenRadius(app):
    drawLabel('Select a radius of infection for your pathogen: ',app.width/4, app.height/4,size = 18, fill = 'black')
    drawLine((app.width/8)*4, (app.height/4), (app.width/8)*7, app.height/4,fill = 'grey')

    drawLabel(str(app.viralRadius),((app.width/8)*4+(app.width/8)*7)/2, app.height/4+25, size = 20)
    drawCircle(app.radiusSelectorCircleX, app.height/4, 10, fill = 'red')

def selectPopulationSize(app):
    drawLabel('Select a size for your population:',app.width/4, (app.height/8)*3,size = 20, fill = 'black')
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
    drawLabel(str(app.initialInfectedCount),((app.width/8)*4+(app.width/8)*7)/2, (app.height/8)*5+25, size = 20)
    drawCircle(app.infectedSelectorCircleX, (app.height/8)*5, 10, fill = 'red')

def selectStartingNumberOfImmune(app):
    drawLabel('Number of individuals initially immune:',app.width/4, (app.height/8)*6,size = 20, fill = 'black')
    drawLine((app.width/8)*4, (app.height/8)*6, (app.width/8)*7, (app.height/8)*6,fill = 'grey')
    drawLabel(str(app.initialVaccinatedCount),((app.width/8)*4+(app.width/8)*7)/2, (app.height/8)*6+25, size = 20)
    drawCircle(app.immuneSelectorCircleX, (app.height/8)*6, 10, fill = 'red')

def sliderSelection(app, mouseX, mouseY):
    if app.populationSelected:
        if ((app.width/8)*4) <= mouseX and mouseX <= ((app.height/8)*7):
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
            elif distanceDotFromStart >= 340 and distanceDotFromStart <=400:
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
    if app.infectedSelected:
        if ((app.width/8)*4) <= mouseX and mouseX <= (app.width/8)*7:
            distanceDotFromStart = distance(mouseX,app.width/2,mouseY, (app.height/8)*5)
            if distanceDotFromStart <= 50:
                app.initialInfectedCount = 1
            elif distanceDotFromStart >= 50 and distanceDotFromStart <=100:
                app.initialInfectedCount =2
            elif distanceDotFromStart >= 150 and distanceDotFromStart <=200:
                app.initialInfectedCount =3
            elif distanceDotFromStart >= 250 and distanceDotFromStart <=300:
                app.initialInfectedCount =4
            elif distanceDotFromStart >= 350 and distanceDotFromStart <=400:
                app.initialInfectedCount = 5
            app.infectedSelectorCircleX = mouseX
    if app.immuneSelected:
        if ((app.width/8)*4) <= mouseX and mouseX <= (app.width/8)*7:
            distanceDotFromStart = distance(mouseX,app.width/2,mouseY, (app.height/8)*6)
            if distanceDotFromStart <= 50:
                app.initialVaccinatedCount = 1
            elif distanceDotFromStart >= 50 and distanceDotFromStart <=100:
                app.initialVaccinatedCount =2
            elif distanceDotFromStart >= 150 and distanceDotFromStart <=200:
                app.initialVaccinatedCount =3
            elif distanceDotFromStart >= 250 and distanceDotFromStart <=300:
                app.initialVaccinatedCount =4
            elif distanceDotFromStart >= 350 and distanceDotFromStart <=400:
                app.initialVaccinatedCount = 5
            app.immuneSelectorCircleX = mouseX