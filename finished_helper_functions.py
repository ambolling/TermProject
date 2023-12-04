from cmu_graphics import *
from person import person

def drawGraph(app):
    rectLeft = 300
    rectTop = 300
    rectWidth = 500
    rectHeight = 300
    drawRect(rectLeft,rectTop,rectWidth,rectHeight, fill = 'white',border = 'black')
    drawLabel('0',260,600,size = 20)
    drawLabel(str(app.populationSize),260,300,size = 20)
    days = len(app.dictChangeOverTimeInfected)
    incrementDays = (rectWidth)//(days-1)
    listInfected =[]
    listHealthy = []
    listImmune = []
    for i in range(1,days+1):
        xVal = rectLeft + (incrementDays*(i-1))
        ammountHealthy = app.dictChangeOverTimeHealthy[i]
        ammountInfected = app.dictChangeOverTimeInfected[i]
        ammountImmune = app.populationSize - (ammountHealthy+ammountInfected)
        yValInfected = rectTop + (rectLeft - (ammountInfected* rectHeight/app.populationSize))
        yValHealthy = rectTop + (rectLeft - (ammountHealthy * rectHeight)/app.populationSize)
        yValImmune = rectTop + (rectLeft - (ammountImmune * rectHeight)/app.populationSize)
        drawCircle(xVal, yValInfected, 8, fill = 'red')
        drawCircle(xVal, yValHealthy, 8, fill = 'green')
        drawCircle(xVal, yValImmune, 8, fill = 'lightBlue')
        if i%2 != 0 and i != days:
            drawLabel(f'Day {i}', rectLeft +(incrementDays*i),640, size = 12) 
        listInfected.append([xVal, yValInfected])
        listHealthy.append([xVal, yValHealthy])
        listImmune.append([xVal, yValImmune])
    for j in range(len(listInfected)-1):
        drawLine(listInfected[j][0],listInfected[j][1],listInfected[j+1][0],listInfected[j+1][1], fill='lightGrey')
    for k in range(len(listHealthy)-1):
        drawLine(listHealthy[k][0],listHealthy[k][1],listHealthy[k+1][0],listHealthy[k+1][1], fill = 'lightGrey')
    for z in range(len(listImmune)-1):
        drawLine(listImmune[z][0],listImmune[z][1],listImmune[z+1][0],listImmune[z+1][1], fill = 'lightGrey')
    drawLabel('Days',540, 675, size = 30)
    drawLabel('Number of People',200, 450, size = 30, rotateAngle=270)
