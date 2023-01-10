#####################
# Name: Keiser Dallas
# Date: 12/20/2022
# CSC 470-001
# Assignment 1: This a Tkinter GUI that draws three 3-D shapes and allows the user to select and manipulate these shapes
#                   using basic scaling, translations, and (XYZ) rotations. The transformation equations utlitized are
#                   based on a LHS, CCW system w/ viewer in -Z direction  
# 
#####################

from math import *
import copy
from tkinter import *


# ***************************** Initialize Pyramid Object ***************************
# Definition  of the five underlying points
apex = [0,50,100]
base1 = [50,-50,50]
base2 = [50,-50,150]
base3 = [-50,-50,150]
base4 = [-50,-50,50]

# Definition of the five polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
frontpoly = [apex,base1,base4]
rightpoly = [apex,base2,base1]
backpoly = [apex,base3,base2]
leftpoly = [apex,base4,base3]
bottompoly = [base1,base2,base3,base4]

# Definition of the object
Pyramid = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
PyramidPointCloud = [apex, base1, base2, base3, base4]
DefaultPyramidPointCloud = copy.deepcopy(PyramidPointCloud)



#**************************** Initializing Cube 1 Object ****************************
# Definition of eight underlying points
lb1 = [-150,-50,50]
lb2 = [-150,-50,150] 
lb3 = [-250,-50,150]
lb4 = [-250,-50,50]
lt1 = [-150,50,50]
lt2 = [-150,50,150]
lt3 = [-250,50,150]
lt4 = [-250,50,50]

# Definition of six polygon faces using meaningful point names
# Polys are defined in clockwise order when viewed from outside
lf = [lt1,lb1,lb4,lt4]
lb = [lt2,lb2,lb3,lt3]
lt = [lt1,lt2,lt3,lt4]
lbt = [lb1,lb2,lb3,lb4]
lr = [lt1,lt2,lb2,lb1]
ll = [lt3,lt4,lb4,lb3]

# Definition of the object
leftCube = [lbt,lf,lt,lb,lr,ll]

# Definition of the Cube's underlying point cloud. No structure, just the points
leftCubePointCloud = [lb1,lb2,lb3,lb4,lt1,lt2,lt3,lt4]
DefaultLeftCubePointCloud = copy.deepcopy(leftCubePointCloud)
 

#*************************** Initializing Cube 2 Object *****************************
# Definition of eight underlying points
rb1 = [250,-50,50]
rb2 = [250,-50,150] 
rb3 = [150,-50,150]
rb4 = [150,-50,50]
rt1 = [250,50,50]
rt2 = [250,50,150]
rt3 = [150,50,150]
rt4 = [150,50,50]

# Definition of six polygon faces using meaningful point names
# Polys are defined in clockwise order when viewed from outside
rf = [rt1,rb1,rb4,rt4]
rb = [rt2,rb2,rb3,rt3]
rt = [rt1,rt2,rt3,rt4]
rbt = [rb1,rb2,rb3,rb4]
rr = [rt1,rt2,rb2,rb1]
rl = [rt3,rt4,rb4,rb3]

# Definition of the object
rightCube = [rbt,rf,rt,rb,rr,rl]

# Definition of the Cube's underlying point cloud. No structure, just the points
rightCubePointCloud = [rb1,rb2,rb3,rb4,rt1,rt2,rt3,rt4]
DefaultRightCubePointCloud = copy.deepcopy(rightCubePointCloud)



#************************************************************************************

# This function resets the pyramid to its original size and location in 3D space
# Note that you have to be careful to update the values in the existing PyramidPointCloud
# structure rather than creating a new structure or just switching a pointer.  In other
# words, you'll need manually update the value of every x, y, and z of every point in
# point cloud (vertex list).
def resetPyramid():
    for i in range(len(PyramidPointCloud)):
        for j in range(3):
            PyramidPointCloud[i][j] = DefaultPyramidPointCloud[i][j]

# This function resets cube1 to its original size and location in 3D space
def resetCube1():
    for i in range(len(leftCubePointCloud)):
        for j in range(3):
            leftCubePointCloud[i][j] = DefaultLeftCubePointCloud[i][j]

# This function resets cube 2 to its original size and location in 3D space
def resetCube2():
    for i in range(len(rightCubePointCloud)):
        for j in range(3):
            rightCubePointCloud[i][j] = DefaultRightCubePointCloud[i][j]

# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
    # Starting with first point
    point = 0
    while(point < len(object)):
        position = 0
        while(position < 3):
            # Add the displacement for each XYZ-coordinate 
            object[point][position] = object[point][position] + displacement[position]
            position+=1
        point +=1


# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object,scalefactor):
    # Calculate reference point
    ref = reference(object)
    # Starting with first point 
    point = 0
    while(point < len(object)):
        position = 0
        while(position < 3):
            # Scale each XYZ-coordinate
            object[point][position] = object[point][position] - ref[position]
            object[point][position] = object[point][position] * scalefactor
            object[point][position] = object[point][position] + ref[position]
            position+=1
        point +=1
            
# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
def rotateZ(object,degrees):
    # Convert degrees to radians
    degrees = radians(degrees)
    # Calculate reference point
    ref = reference(object)
    # Starting with first point
    point = 0
    while(point < len(object)):
        # Move using reference point
        object[point][0] -= ref[0]
        object[point][1] -= ref[1]
        object[point][2] -= ref[2]
        
        # Calculate X
        tempX = float(object[point][0] * cos(degrees) - object[point][1] * sin(degrees))
        # Calculate Y
        tempY = float(object[point][0] * sin(degrees) + object[point][1] * cos(degrees))
        # Calculate Z
        object[point][2] = object[point][2]

        # Move back using reference point
        object[point][0] = tempX + ref[0]
        object[point][1] = tempY + ref[1]
        object[point][2] += ref[2]
        point +=1
    
# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object,degrees):
    # Convert degrees to radians
    degrees = radians(degrees)
    # Calculate reference point
    ref = reference(object)
    # Starting with first point
    point = 0
    while(point < len(object)):
        # Move using reference point
        object[point][0] -= ref[0]
        object[point][1] -= ref[1]
        object[point][2] -= ref[2]
        
        # Calculate x
        tempX = float(object[point][0] * cos(degrees) + object[point][2] * sin(degrees))
        # Calculate Y
        object[point][1] = object[point][1]
        # Calculate Z
        tempZ = float(- object[point][0] * sin(degrees) + object[point][2] * cos(degrees))

        # Move back using reference point
        object[point][0] = tempX + ref[0]
        object[point][1] += ref[1]
        object[point][2] = tempZ + ref[2]
        
        point +=1

# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object,degrees):
    # Convert degrees to radians
    degrees = radians(degrees)
    # Calculate reference point
    ref = reference(object)
    # Starting with first point
    point = 0
    while(point < len(object)):
        # Move using reference point
        object[point][0] -= ref[0]
        object[point][1] -= ref[1]
        object[point][2] -= ref[2]
        
        # Calculate X
        object[point][0] = object[point][0]
        # Calculate Y
        tempY = float(object[point][1] * cos(degrees) - object[point][2] * sin(degrees))
        # Calculate Z
        tempZ = float(object[point][1] * sin(degrees) + object[point][2] * cos(degrees))

        # Move back using reference point
        object[point][0] += ref[0]
        object[point][1] = tempY + ref[1]
        object[point][2] = tempZ + ref[2]

        point +=1


# Draws all shapes 
def createScene():
    for object in scene:
        drawObject(object)
        
# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(object):
    # If the object is the user selected shape, draw with red lines
    if(object == scene[selected]):
        for polygon in object:
            drawPoly(polygon, True)
    # Otherwise draw with default black lines
    else:
        for polygon in object:
            drawPoly(polygon, False)
    
# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
# It takes in an additional boolean to determine if we are drawing the user selected shape
def drawPoly(poly,ifSelected):
    # For each point of the polygon, starting with the first
      i = 0
      while(i < len(poly)):
          # Connect the last point with the first point
          if(i == len(poly)-1):
              drawLine(poly[i], poly[0],ifSelected)
          # Otherwise draw line to the next connecting point
          else:
              drawLine(poly[i], poly[i+1],ifSelected)
          i+=1


# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def drawLine(start,end,ifSelected):
    # Take the starting and ending points,
    # Calculate their corresponding projection points, and
    # Convert those points to display coordinates
    startDisplay = convertToDisplayCoordinates(project(start))
    endDisplay = convertToDisplayCoordinates(project(end))
    # Check to see if this is the user selected shape
    if(ifSelected == True):
        # Color the lines red 
        w.create_line(startDisplay[0], startDisplay[1], endDisplay[0], endDisplay[1], fill="red")
    else:
        # Otherwise leave the lines black by default
        w.create_line(startDisplay[0], startDisplay[1], endDisplay[0], endDisplay[1])

# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
    # Create a project point 
    ps = []
    # Take each coordinate in the point, and calculate their corresponding projection point
    ps = [float(d * (x/(d+point[2]))) for x in point]
    return ps

# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as 
# they are only used in rendering.
def convertToDisplayCoordinates(point):
    # Create an empty display coordinate
    displayXY = [0 for x in range(2)]
    # Set the X and Y display coordinates
    displayXY[0] = (CanvasWidth/2) + point[0]
    displayXY[1] = (CanvasHeight/2) - point[1]
    return displayXY

# This function finds and returns a 3D reference point for a given object
def reference(object):
    # Min and max values to compare 
    xMin = 9999
    xMax = -9999
    yMin = 9999
    yMax = -9999
    zMin = 9999
    zMax = -9999
    # Seach for the minimum values
    for point in object:
        if(point[0] < xMin):
            xMin = point[0]
        if(point[1] < yMin):
            yMin = point[1]
        if(point[2] < zMin):
            zMin = point[2]

    # Search for the max values
    for point in object:
        if(point[0] > xMax):
            xMax = point[0]
        if(point[1] > yMax):
            yMax = point[1]
        if(point[2] > zMax):
            zMax = point[2]
    # Calculate center X, Y, and Z
    centerX = float((xMin + xMax)/2)
    centerY = float((yMin + yMax)/2)
    centerZ = float((zMin + zMax)/2)

    # Create reference point and return
    ref = [centerX, centerY, centerZ]
    return ref 

# **************************************************************************
# Everything below this point implements the interface
def reset():
    w.delete(ALL)
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    # If cube 1
    if(object == scene[0]):
        resetCube1()
    # If pyramid
    elif(object == scene[1]):
        resetPyramid()
    # If cube 3
    elif(object == scene[2]):
        resetCube2()
    createScene()
    

def larger():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube1
    if(object == scene[0]):
        scale(leftCubePointCloud,1.1)
    # If pyramid
    elif(object == scene[1]):
        scale(PyramidPointCloud,1.1)
    # If cube 3
    elif(object == scene[2]):
        scale(rightCubePointCloud,1.1)
    createScene()

def smaller():
    # Figuring out whic shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        scale(leftCubePointCloud,.9)
    # If pyramid
    elif(object == scene[1]):
        scale(PyramidPointCloud,.9)
    # If cube 2
    elif(object == scene[2]):
         scale(rightCubePointCloud,.9)
    createScene()
   

def forward():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(leftCubePointCloud,[0,0,5])
    # If pyramid
    elif(object == scene[1]):
        translate(PyramidPointCloud,[0,0,5])
    # If cube 2
    elif(object == scene[2]):
        translate(rightCubePointCloud,[0,0,5])
    createScene()
  

def backward():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(leftCubePointCloud,[0,0,-5])
    # If pyramid
    elif(object == scene[1]):
        translate(PyramidPointCloud,[0,0,-5])
    # if cube 2
    elif(object == scene[2]):
        translate(rightCubePointCloud,[0,0,-5])
    createScene()
  
def left():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(leftCubePointCloud,[-5,0,0] )
    # if pyramid
    elif(object == scene[1]):
        translate(PyramidPointCloud,[-5,0,0])
    # If cube 2
    elif(object == scene[2]):
        translate(rightCubePointCloud,[-5,0,0])
    createScene()
  
def right():
    # Figuring out which shape is selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(leftCubePointCloud,[5,0,0])
    # If pyramid 
    elif(object == scene[1]):
        translate(PyramidPointCloud,[5,0,0])
    # If cube 2
    elif(object == scene[2]):
        translate(rightCubePointCloud,[5,0,0])
    createScene()
  

def up():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(leftCubePointCloud,[0,5,0])
    # If pyramid
    elif(object == scene[1]):
        translate(PyramidPointCloud,[0,5,0])
    # If cube 2
    elif(object == scene[2]):
        translate(rightCubePointCloud,[0,5,0])
    createScene()

def down():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(leftCubePointCloud,[0,-5,0])
    # If pyrmaid
    elif(object == scene[1]):
        translate(PyramidPointCloud,[0,-5,0])
    # If cube 2
    elif(object == scene[2]):
        translate(rightCubePointCloud,[0,-5,0])
    createScene()


def xPlus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateX(leftCubePointCloud,5)
    # If pyramid
    elif(object == scene[1]):
        rotateX(PyramidPointCloud,5)
    # If cube 2
    elif(object == scene[2]):
        rotateX(rightCubePointCloud,5)
    createScene()


def xMinus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateX(leftCubePointCloud,-5)
    # If pyramid
    elif(object == scene[1]):
        rotateX(PyramidPointCloud,-5)
    # if cube 2
    elif(object == scene[2]):
        rotateX(rightCubePointCloud,-5)
    createScene()

def yPlus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateY(leftCubePointCloud,5)
    # If pyramid
    elif(object == scene[1]):
        rotateY(PyramidPointCloud,5)
    # If cube 2
    elif(object == scene[2]):
        rotateY(rightCubePointCloud,5)
    createScene()

def yMinus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateY(leftCubePointCloud,-5)
    # If pyramid
    elif(object == scene[1]):
        rotateY(PyramidPointCloud,-5)
    # If cube 2
    elif(object == scene[2]):
        rotateY(rightCubePointCloud,-5)
    createScene()

def zPlus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateZ(leftCubePointCloud,5)
    # If pyrmaid
    elif(object == scene[1]):
        rotateZ(PyramidPointCloud,5)
    # If cube 2
    elif(object == scene[2]):
        rotateZ(rightCubePointCloud,5)
    createScene()

def zMinus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
         rotateZ(leftCubePointCloud,-5)
    # If pyramid
    elif(object == scene[1]):
         rotateZ(PyramidPointCloud,-5)
    # If cube 2
    elif(object == scene[2]):
        rotateZ(rightCubePointCloud,-5)
    createScene()

    
# Arrow key controls for <left>
def lKey(event):
    # Grabs the index of the current user selected shape
    global selected
    # If the shape is furtherest left, move to furtherest right shape
    if(selected == 0):
        selected = 2
    # Otherwise, move to the next left shape
    else:
        selected -= 1
    createScene()

# Arrow key controls for <right>    
def rKey(event):
    # Grabs the index of the current user selected shape
    global selected
    # If the shape is furtherest right, move to the furtherest left shape
    if(selected == 2):
        selected = 0
    # Otherwise, move to the next right shape
    else:
        selected += 1
    createScene()



root = Tk()
# Create '<' and '>' key bindings w/ callback functions
root.bind('<Left>',lKey)
root.bind('<Right>', rKey)
outerframe = Frame(root)
outerframe.pack()
# Canvas dimensions
CanvasWidth = 600
CanvasHeight = 600
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
w.pack()





controlpanel = Frame(outerframe)
controlpanel.pack()

resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translatecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
translatecontrols.pack(side=LEFT)

translatecontrolslabel = Label(translatecontrols, text="Translation")
translatecontrolslabel.pack()

forwardButton = Button(translatecontrols, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translatecontrols, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translatecontrols, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translatecontrols, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="UP", command=up)
upButton.pack(side=LEFT)

downButton = Button(translatecontrols, text="DN", command=down)
downButton.pack(side=LEFT)

rotationcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
rotationcontrols.pack(side=LEFT)

rotationcontrolslabel = Label(rotationcontrols, text="Rotation")
rotationcontrolslabel.pack()

xPlusButton = Button(rotationcontrols, text="X+", command=xPlus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotationcontrols, text="X-", command=xMinus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotationcontrols, text="Y+", command=yPlus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotationcontrols, text="Y-", command=yMinus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotationcontrols, text="Z+", command=zPlus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotationcontrols, text="Z-", command=zMinus)
zMinusButton.pack(side=LEFT)

#************ MAIN ****************

# Viewer distance from screen
d = 500
# Create a visually ordered list of objects 
scene = [leftCube, Pyramid, rightCube]
# Automatically set the selected shape for the first image
selected = 1
# Generate the first image of objects
createScene()
# Launch the GUI
root.mainloop()



