# events-example0.py
# Barebones timer, mouse, and keyboard events
from tkinter import *
import math
import random
import numpy as np
import math

####################################
# customize these functions
####################################

    

def init(data):
    data.pPos = [0,0,0]
    data.pDir = [1,0,0]
    data.angleX = 0
    data.angleZ = 0
    data.coordArray = [[np.asarray([4,1,-1]),np.asarray([4,1,1]),np.asarray([6,1,1]),np.asarray([6,1,-1])],\
    [np.asarray([4,-1,1]),np.asarray([4,1,1]),np.asarray([6,1,1]),np.asarray([6,-1,1])],\
    [np.asarray([4,1,-1]),np.asarray([4,1,1]),np.asarray([4,-1,1]),np.asarray([4,-1,-1])]]
    pass
    

def mousePressed(event, data):
    data.mx = event.x
    data.my = event.y
    pass

def keyPressed(event, data):
	# move wasd
	if event.keysym == "w":
		data.pPos += np.asarray((data.pDir[0],data.pDir[1],0)) / 10
	if event.keysym == "s":
		data.pPos -= np.asarray((data.pDir[0],data.pDir[1],0)) / 10
	if event.keysym == "d":
		data.pPos += np.asarray((data.pDir[1],-data.pDir[0],0)) / 10
	if event.keysym == "a":
		data.pPos -= np.asarray((data.pDir[1],-data.pDir[0],0)) / 10

	# move up and down
	if event.keysym == "q":
		data.pPos += np.asarray((0,0,.1))
	if event.keysym == "e":
		data.pPos -= np.asarray((0,0,.1))

	# turn
	if event.keysym == "Left":
		data.angleX += 3.1415/180
	if event.keysym == "Right":
		data.angleX -= 3.1415/180
	if event.keysym == "Up":
		data.angleZ += 3.1415/180
		data.angleZ = min(data.angleZ,3.14159265/2)
	if event.keysym == "Down":
		data.angleZ -= 3.1415/180
		data.angleZ = max(data.angleZ,-3.14159265/2)
	data.angleX = (data.angleX) % (2*3.14159265)
	data.pDir = [math.cos(data.angleX)*math.cos(data.angleZ),math.sin(data.angleX)*math.cos(data.angleZ),math.sin(data.angleZ)]


	pass

def timerFired(data):
    
    pass

def renderPolygon(data,coordinates):
	height = data.height
	width = data.width
	canvasCoords = []
	pPos = np.asarray(data.pPos)
	pDir = np.asarray(data.pDir)
	for point in coordinates:
		# calculate distance from the player to the plane perpendicular to their view containing the point
		dPToPlane = np.dot(pDir,point-pPos)
		if dPToPlane < 0:
			return None
		# calculate X distance from perp projection of player onto perpendicular plane containing the point
		dX = np.dot((pDir[1],-pDir[0]),point[0:2]-pPos[0:2])/np.linalg.norm(pDir[0:2])
		dY = (abs(np.linalg.norm(pPos-point)**2-dPToPlane**2-dX**2))**0.5 # pythagorean theorem
		# project person onto perp plane
		t = np.dot(pDir,point-pPos)
		# if z coordinate of point is higher, then dY is pos, else neg
		z = t*pDir[2]+pPos[2]
		if z<point[2]:
			dY = -dY
		# size of viewing square at the distance of the point
		sqSize = dPToPlane*2
		canvasCoords.append((width*dX/sqSize+width/2,height*dY/sqSize+height/2))
	return canvasCoords

def redrawAll(canvas, data):
	fill = "red"
	for coordinates in data.coordArray:
		coords = renderPolygon(data,coordinates)
		if coords != None:
			canvas.create_polygon(coords[0][0],coords[0][1],coords[1][0],coords[1][1],coords[2][0],coords[2][1],coords[3][0],coords[3][1],fill=fill)
			fill = "blue" if (fill == "red") else "green"
	        # canvas.create_rectangle(50-data.xShift,50-data.yShift, 2 * data.width-50-data.xShift,2 * data.height-50-data.yShift,width = 10)
	        # canvas.create_oval(i[0]-i[2] * 1 / 5,i[1]-i[2] * 1 / 5, i[0]+i[2] * 1 / 5,i[1]+i[2] * 1 / 5, fill="red")
	        # canvas.create_text(50, data.height - 50, text = "Score = %d" % data.score,anchor = SW, font="helvetica 20", fill = "red")
	pass

####################################
# use the run function as-is
####################################

def run(width=800, height=800):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)
