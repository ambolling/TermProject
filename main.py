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

def generatePopulation(app):
    for i in range(100):
        xVal = random.randint(app.populationLeftBoundary,app.populationRightBoundary)
        yVal = random.randint(app.populationTopBoundary,app.populationBottomBoundary)
        app.populationHealthyMembers.append([xVal,yVal])

def redrawAll(app):
    generatePopulation(app)
    generateInfectedMember(app)
    for pair in app.populationHealthyMembers:
        drawCircle(pair[0],pair[1],10, fill = 'green')
    for pair in app.populationInfectedMembers:
        drawCircle(pair[0],pair[1],10, fill = 'red')

def generateInfectedMember(app):
    centerPeople = []
    boardCenterX = (app.populationRightBoundary+app.populationLeftBoundary)//2 
    boardCenterY = (app.populationTopBoundary+app.populationBottomBoundary)//2
    #randomly infect someone in the center of the board 
    for person in app.populationHealthyMembers:
        if distance(person[0], boardCenterX, person[1],boardCenterY) < 100:
            app.populationInfectedMembers.append(person)
            break

def distance(x1,x2,y1,y2):
    return (((x1-x2)**2+(y1-y2)**2)**.5)



def main():
    runApp(width = 1000, height = 1000)

main()