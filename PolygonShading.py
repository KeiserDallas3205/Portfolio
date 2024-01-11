##############################
#
# Name: Keiser Dallas
# Date: 2/7/2023
# CSC 470- 001
# Assignment 3: This program is an extension of Assignment 2 that projected a 3D shape onto the screen along w/
#                   3D transformations and rotations in a LHS CCW system w/ viewer in -Z. Also, there is
#                   backface culling implemented into 3 draw modes:
#                           1) Wireframe only
#                           2) Polygon Fill w/ Wireframe
#                           3) Polygon Fill only
#
#                   The new additions include:
#                           - 1 singular cylinder object
#                           - Phong Illumination Model
#                           - Flat Shading 
#                           - Gouraud Shading
#                           - Phong Shading 
#
#############################

from math import *
import copy
from tkinter import *

# ***************************** Initialize Cylinder Object ***************************
# Definition of the 16 underlying points
front1 = [-50,120.7107,50]
front2 = [50,120.7107,50]
front3 = [120.7107,50,50]
front4 = [120.7107,-50,50]
front5 = [50,-120.7107,50]
front6 = [-50,-120.7107,50]
front7 = [-120.7107,-50,50]
front8 = [-120.7107,50,50]
back1 = [-50,120.7107,450]
back2 = [50,120.7107,450]
back3 = [120.7107,50,450]
back4 = [120.7107,-50,450]
back5 = [50,-120.7107,450]
back6 = [-50,-120.7107,450]
back7 = [-120.7107,-50,450]
back8 = [-120.7107,50,450]
# Definition of the ten polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
northPoly = [front1, back1, back2, front2]
northEastPoly = [front2, back2, back3, front3]
eastPoly = [front3, back3, back4, front4]
southEastPoly = [front4, back4, back5, front5]
southPoly = [front5, back5, back6, front6]
southWestPoly = [front6, back6, back7, front7]
westPoly = [front7, back7, back8, front8]
northWestPoly = [front8, back8, back1, front1]
frontPoly = [front1, front2, front3, front4, front5, front6, front7, front8]
backPoly = [back1, back8, back7, back6, back5, back4, back3, back2]
# Definition of the cylinder object
cylinder = [northPoly, northEastPoly, eastPoly, southEastPoly, southPoly, southWestPoly, westPoly, northWestPoly,
frontPoly, backPoly]

# Definition of the cylinder's underlying point cloud. No structure, just the points
cylinderPointCloud = [front1,front2,front3,front4,front5,front6,front7,front8,back1,back2,back3,back4,back5,back6,back7,back8]
DefaultCylinderPointCloud = copy.deepcopy(cylinderPointCloud)

# Cylinder color
cylinderColor = ['red','yellow','pink','blue','white','black','green','orange','red','yellow']


#************************************************************************************

# This function resets cylinder to its original size and location in 3D space
def resetCylinder():
    for i in range(len(cylinderPointCloud)):
        for j in range(3):
            cylinderPointCloud[i][j] = DefaultCylinderPointCloud[i][j]

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
        rotX = float(object[point][0] * cos(degrees) - object[point][1] * sin(degrees))
        # Calculate Y
        rotY = float(object[point][0] * sin(degrees) + object[point][1] * cos(degrees))
        # Calculate Z
        object[point][2] = object[point][2]

        # Move back using reference point
        object[point][0] = rotX + ref[0]
        object[point][1] = rotY + ref[1]
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
        rotX = float(object[point][0] * cos(degrees) + object[point][2] * sin(degrees))
        # Calculate Y
        object[point][1] = object[point][1]
        # Calculate Z
        rotZ = float(- object[point][0] * sin(degrees) + object[point][2] * cos(degrees))

        # Move back using reference point
        object[point][0] = rotX + ref[0]
        object[point][1] += ref[1]
        object[point][2] = rotZ + ref[2]
        
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
        rotY = float(object[point][1] * cos(degrees) - object[point][2] * sin(degrees))
        # Calculate Z
        rotZ = float(object[point][1] * sin(degrees) + object[point][2] * cos(degrees))

        # Move back using reference point
        object[point][0] += ref[0]
        object[point][1] = rotY + ref[1]
        object[point][2] = rotZ + ref[2]

        point +=1


# Draws all shapes 
def createScene():
    for object in scene:
        # Create zBuffer[][] variable filled w/ max distance values
        # Initialized for each scene 
        buffer = [[d for x in range(CanvasWidth)]for s in range(CanvasHeight)]
        drawObject(object,mode,buffer)
    
# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(object,mode,zBuffer):

    # Set the color for regular Polygon Fill
    color = cylinderColor

    # Wireframe
    if(mode == 1):
        
        # If the object is the user selected shape, draw with red lines
        if(object == scene[selected]):
            for polygon in object:
                drawPoly(polygon, True)
        # Otherwise draw with default black lines
        else:
            for polygon in object:
                drawPoly(polygon, False)

    # Polygon Fill w/ wireframe
    elif(mode == 2):
        # If the object is the user selected shape, draw with red lines
        if(object == scene[selected]):
            nTable = normalTable(object)
            # Fill polygon, then draw the lines
            for polygon,c in zip(object,color):
                fillPoly(polygon,c,zBuffer,nTable)
                drawPoly(polygon, True)
        # Otherwise draw with default black lines
        else:
            nTable = normalTable(object)
            # Fill the polygon, then draw the lines
            for polygon,c in zip(object,color):
                fillPoly(polygon,c,zBuffer,nTable)
                drawPoly(polygon, False)

    # Polygon Fill
    elif(mode == 3):
        nTable = normalTable(object)
        # Fill the polygon
        for polygon,c in zip(object,color):
            fillPoly(polygon,c,zBuffer,nTable)

    # Flat-Shading
    elif(mode == 4):
        nTable = normalTable(object)
        # Calculate the color, then fill the polygon
        for polygon in object:
            color = flatShade(polygon,Ia,Ip,Kd,Ks,specIndex,L,V)
            fillPoly(polygon,color,zBuffer,nTable)

    # Gouraud Shading
    elif(mode == 5):
        nTable = normalTable(object)
        for polygon in object:
            # Shade the polygon
            GouraudShade(polygon,zBuffer,nTable)

    # Phong Shading
    elif(mode == 6):
        nTable = normalTable(object)
        for polygon in object:
            # Shade the polygon
            PhongShade(polygon,zBuffer,nTable)
        
               
 
 
    
# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
# It takes in an additional boolean to determine if we are drawing the user selected shape
def drawPoly(poly,ifSelected):
    # Check if polygon is visible
    if(backFace(poly) == True):
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

# This funcion is the exact same as above EXCEPT it rounds the x and y coordinates before
# passing the NEW list of points. Also, it saves the Zps coordinate for the zbuffer implementation.
# This version is used in the Polygon Fill algorithm
def cTDC(point):
    # Create an empty display coordinate
    displayXY = [0 for x in range(3)]
    # Set the X and Y display coordinates
    # Round the x and y before returning the coordinates 
    displayXY[0] = round((CanvasWidth/2) + point[0])
    displayXY[1] = round((CanvasHeight/2) - point[1]) 
    displayXY[2] = point[2]
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


#************* Back-Face Culling Methods ***********************************

# This function takes two points(start,end)
# Returns a vector (end - start)
def vector(start,end):
    v = []
    v = [z-x for x,z in zip(start,end)]
    return v 

# This function computes the magnitude of a vector
# Returns a scalar
def magnitude(vector):
    i = 0
    total = 0
    while(i < len(vector)):
        total += pow(vector[i],2)
        i += 1
    total = sqrt(total)
    return total

# This function computes the dot product
# Returns a scalar
def dot(A,B):
    product = 0
    for x,z in zip(A,B):
        product += (x*z)
    return product


# This function computes the cross product of two variables
# Returns a vector
def crossP(P,Q):
    cross = [0 for x in range(len(P))]
    cross[0] = (P[1]*Q[2])-(P[2]*Q[1])
    cross[1] = (P[2]*Q[0])-(P[0]*Q[2])
    cross[2] = (P[0]*Q[1])-(P[1]*Q[0])
    return cross
    

# This function normalizes any given vector
# Returns its corresponding unit vector
def norm(vector):
    vNorm = [(x/magnitude(vector)) for x in vector]
    return vNorm

# Function calculates the normal of a polygon
# Returns an normalized unit vector [x,y,z]
def calculateNormal(polygon):
    P = vector(polygon[0],polygon[1])
    Q = vector(polygon[0],polygon[2])
    N = norm(crossP(P,Q))
    return(N)


# This function takes in a polygon, and determines whether it is the current backface
# Returns a boolean 'visible' that determines if the polygon should be drawn
def backFace(polygon):
    visible = False
    view = [0,0,-d]
    N = calculateNormal(polygon)
    D = dot(N,polygon[0])
    if((dot(N,view) - D)> 0):
        visible = True
    return visible
    

# **************************** Polygon Filling w/ zBuffer Methods *************************************
# This function takes two 2D points (start,end), and returns their inverse slope
# Returns a (+/-) floating point number 
def invSlope(start,end):
    # Check for 0 divisor or horizontal lines
    if(end[1] - start[1] == 0 or end[1] == start[1]):
        # This edge shouldn't be in the table
        invSlope = None
    else:
        # Calculate inverse slope
        invSlope = (end[0] - start[0])/(end[1] - start[1])
        
    return invSlope

# This function takes two points,(start,end), and computes their change in z (dz)
# Returns a (+/-) floating point number 
def dz(start,end):
    # Check for 0 divsor
    if(end[1] - start[1] == 0):
        # This shouldn't be in the table
        dz = None
    else:
        # Calculate dz
        dz = (end[2] - start[2])/(end[1]-start[1])
    return dz



# Function that generates a polygon fill table
# Returns a dictionary:
#   key -> edge
#   value -> [xstart,ystart,yend,invSlope,zStart,dz]
def fillTable(polygon,nTable):
    # Create empty dictionary to store fill table
    table = {}
    
    # Create an edge 
    vertex = 0
    edge = 0
    while(edge < len(polygon) and vertex < len(polygon)):
        
        # If last vertex, connect to first vertex; Otherwise continue
        if(vertex == len(polygon)-1):
            # Precompute the required values
            xStart,yStart,yEnd,invSlope,zStart,deltaz = boundaries(polygon[vertex],polygon[0])
            intStart, intEnd, dI,nStart,nEnd,dN = shaders(polygon[vertex],polygon[0],nTable)
        else:
            # Precompute the required values
            xStart,yStart,yEnd,invSlope,zStart,deltaz = boundaries(polygon[vertex],polygon[vertex+1])
            intStart,intEnd,dI,nStart,nEnd,dN = shaders(polygon[vertex],polygon[vertex+1],nTable)

        # If edge does not have a zero divisor or horizontal line, then add to the fill table
        if(invSlope != None):
            table[edge] = [xStart,yStart,yEnd,invSlope,zStart,deltaz,intStart,intEnd,dI,nStart,nEnd,dN]
            edge += 1
        
        # Move to next point 
        vertex += 1

    # Sort the dictionary by yStart values
    sortedTable = dict(sorted(table.items(),key=lambda x:x[1][1]))
    
    # Return the dictonary/fill table
    return sortedTable


# Function that takes in two points of a edge and compute:
#       xStart, yStart, yEnd, inverse slope, zStart, dz, intStart, intEnd, dI
# It returns all those values in that order 
def boundaries(p1,p2):
    # Figure out which has the smallest y value
    if(p1[1] < p2[1]):
        start = p1
        end = p2
    else:
        start = p2
        end = p1

    # Set xStart, yStart, yEnd, zStart
    xStart = start[0]
    yStart = start[1]
    yEnd = end[1]
    zStart = start[2]

    # Compute inverse slope
    inv = invSlope(start,end)

    # Compute dz
    deltaz = dz(start,end)

    

    return xStart,yStart,yEnd,inv,zStart,deltaz

# Function takes an individual polygon, color, and zBuffer
# fills the polygon pixel by pixel one horizontal line at a time
# with the specificed color. Also, uses zBuffer to perform occlusion by giving
# pixels color priority based on relative Zps.  
def fillPoly(poly,color,zBuffer,nTable):
    # Check if polygon is visible
    if(backFace(poly) == True):

        # Convert polygon vertices to display coordinates
        # Round the coordinates 
        displayPoly = [cTDC(project(vertex)) for vertex in poly]

        # Compute the fill table for the polygon
        edgeTable = fillTable(displayPoly,nTable)

        # List of the edges in order
        keys = [s for s in edgeTable.keys()]

        # Check if table is not empty
        if(bool(edgeTable) == True):

            # Smallest y value in table
            firstFillLine = edgeTable.get(keys[0])[1]
            
            # Create a temporary list with all yEnd values
            # Set the lastFillLine equal to the larget of the list
            tempList = [edgeTable.get(x)[2] for x in edgeTable.keys()]
            lastFillLine = max(tempList)


            # Indices for the first, second, and next edge
            I = 0
            J = 1
            Next = 2

            # Paint a fill LINE by selecting all picxels between two edges
            EdgeIX = edgeTable.get(keys[I])[0]
            EdgeJX = edgeTable.get(keys[J])[0]
            EdgeIZ = edgeTable.get(keys[I])[4]
            EdgeJZ = edgeTable.get(keys[J])[4]

            # Paint one fill line at a time
            for y in range(firstFillLine,lastFillLine+1):

                # Determine which edge is left and right
                if(EdgeIX < EdgeJX):
                    LeftX = EdgeIX
                    LeftZ = EdgeIZ
                    RightX = EdgeJX
                    RightZ = EdgeJZ
                    
                else:
                    LeftX = EdgeJX
                    LeftZ = EdgeJZ
                    RightX = EdgeIX
                    RightZ = EdgeIZ

                # Initial Z for current fill line
                z = LeftZ

                # Compute dz for the fill line. Can be 0 if line is 1 pixel long
                if((RightZ - LeftZ) != 0):
                    dzFillLine = (RightZ - LeftZ)/(RightX - LeftX)
                else:
                    dzFillLine = 0
                    
                # Paint a single pixel at a time
                for x in range(round(LeftX),round(RightX+1)):
                    # Check the pixel Zps for color priority
                    if(z < zBuffer[x][y]):
                        # Color the pixel
                        w.create_line(x,y,x+1,y,fill=color)
                        # Store that pixel ZpS
                        zBuffer[x][y] = z
                    # Update the new Zps
                    z += dzFillLine
                    

                # Update the x and z values of edges I and J for the next fill line
                EdgeIX = EdgeIX + edgeTable.get(keys[I])[3]
                EdgeJX = EdgeJX + edgeTable.get(keys[J])[3]
                EdgeIZ += edgeTable.get(keys[I])[5]
                EdgeJZ += edgeTable.get(keys[J])[5]

                # Upon reaching the bottom of an edge, switch out with next available
                if((y >= edgeTable.get(keys[I])[2]) and (y < lastFillLine)):
                    I = Next
                    EdgeIX = edgeTable.get(keys[I])[0]
                    EdgeIZ = edgeTable.get(keys[I])[4]
                    Next +=1
                if((y >= edgeTable.get(keys[J])[2]) and (y < lastFillLine)):
                    J = Next
                    EdgeJX = edgeTable.get(keys[J])[0]
                    EdgeJZ = edgeTable.get(keys[J])[4]
                    Next +=1
    
#********************************** General Shading Methods ********************************

# Constants for calculations

Ia = .3 # Intensity of ambient light
Ip = .7 # Intensity of point light
L = [1,1,-1] # Point light vector
V = [0,0,1] # View vector
Kd = 0.5 # Constant of diffusion
Ks = 0.5 # Constant of specular
specIndex = 4 # Specular index of object

# Calculate a 3D reflection vector, R, given surface normal, N, and lighting vector, L
# Retuns a vector [x,y,z]
def reflect(N,L):
    R = []
    N = norm(N)
    L = norm(L)

    # Calculate the denominator of reflection equation
    twoCosPhi = 2 * dot(N,L)

    # If angle(theta) is less than 90 degrees
    if(twoCosPhi > 0):
        for i in range(3):
            R.append(N[i] - (L[i] / twoCosPhi))
    # If theta equals 90 degrees
    elif(twoCosPhi == 0):
        for i in range(3):
            R.append(-L[i])
    # If theta is greater than 90 degrees
    else:
        for i in range(3):
            R.append(-N[i] + (L[i] / twoCosPhi))

    return norm(R)

# Generate a color hex code string from the illumination components
# Returns a full color hex code 'FFFFFF'
def triColorHexCode(ambient,diffuse,specular):
    # Checks for very small specular and diffuse contribution to eliminate white spots 
    if(diffuse < 0.00001):
        diffuse = 0
    if(specular < 0.00001):
        specular = 0
    combinedColorCode = colorHexCode(ambient + diffuse + specular)
    specularColorCode = colorHexCode(specular)
    colorString = '#' + specularColorCode + combinedColorCode + specularColorCode
    return colorString


# Helper function that checks the formatting of color code
# Returns a partial color hex code 'FF'
def colorHexCode(intensity):
    # Eliminates returning 'non-existent' colors
    # Total intensity cannot exceed 1
    if(intensity > 1):
        intensity = 1
    hexString = str(hex(round(255 * intensity)))
    # Illumination intensity should not be negative
    if(hexString[0] == '-'):
        trimmedHexString = '00'
    else:
        # Get rid of 0x at beginning
        trimmedHexString = hexString[2:]

        # Convert single-digit hex string to two-digit hex string
        if(len(trimmedHexString) == 1):
            trimmedHexString = '0' + trimmedHexString

        # We will use green for our monochrome color system
    return trimmedHexString


# Function calculates the ambient component
# Takes in intensity of ambient light and the constant of diffusion
# Returns a floating point between 0-1
def ambient(Ia,Kd):
    return Ia * Kd

# Function calculates the diffusion component
# Takes in intensity of point light, constant of diffusion, surface normal, and lighting vector
# Returns a floating point between 0-1
def diffuse(Ip,Kd,N,L):
    if(dot(N,L) < 0):
        return 0
    else:
        return Ip * Kd * dot(N,L)

# Function calculates the specular component
# Takes in intensity of point light, constant of specular, specular index,reflection vector, and view vector
# Returns a floating point between 0-1
def specular(Ip,Ks,specIndex,R,V):
    if(dot(R,V) < 0):
        return 0
    else:
        return Ip * Ks * ((dot(R,V))**specIndex)

# ********************** Flat-Shading *************************************
# Function takes in a polygon and uses its first 3 vertices to calculate the surface normal
# That surface nornal is used in a series of equations to get a specific color
# Returns a color hex string
def flatShade(polygon,Ia,Ip,Kd,Ks,specIndex,L,V):
  
    # Find the surface normal of the polygon
    N = calculateNormal(polygon)
    

    # Find the reflection
    R = reflect(N,L)

    # Calculate ambient, diffuse, and specular
    amb = ambient(Ia,Kd)
    diff = diffuse(Ip,Kd,N,L)
    spec = specular(Ip,Ks,specIndex,R,V)

    # Get the hex string for the determined color
    color = triColorHexCode(amb,diff,spec)

    return color
# *************************************** Gouraud Shading *********************************

# Takes in an object and calculates the average normal of each vertex in its REGULAR coordinates
# Then stores the vertex normal in a dictionary linked to its DISPLAY coordinates
#       str(Displayvertex) -> average vertex normal
# Returns the dictionary
def normalTable(object):
    # Create empty dictionary
    table = {}
    # Check each vertex in each polygon, EXCEPT endcaps 
    for polygon in object:
        if(polygon != (frontPoly or backPoly)):
    
            # Calculate the display vertices
            displayPoly = [cTDC(project(vertex)) for vertex in polygon]
            
            for vertex,displayVertex in zip(polygon,displayPoly):
                # Calculate the normal of the normal vertex
                normal = avgNormal(vertex,object)
                # Map it to the display vertex
                table[str(displayVertex)] = normal
    return table

# Function takes in a vertex and an object
# Calculates the average normal of that vertex using the object
# Returns the sum, a normalized unit vector: [x,y,z]
def avgNormal(vertex,object):
    sum = [0,0,0]
    # Check every polygon within the object, EXCEPT endcaps
    for polygon in object:
        if(polygon != (frontPoly or backPoly)):
             # If the vertex is in that polygon,
            if(vertex in polygon):
                # Then calculats its normal and add to the sum
                normal = calculateNormal(polygon)
                sum = [(sum[i]+ normal[i]) for i in range(len(sum))]
    return norm(sum)

# Function takes in two points and normal table, then determines which is the start and end
# Afterwards, it computes the required values for various Gouraud and Phong shading
# Returns a intStart,intEnd,dI,nStart,nEnd, and dN
def shaders(p1,p2,table):
    # Figure out which has the smallest y value
    if(p1[1] < p2[1]):
        start = p1
        end = p2
    else:
        start = p2
        end = p1

    # Get the intensities of (start,end) 
    intStart = Intensity(table.get(str(start)),Ia,Ip,Kd,Ks,specIndex,L,V)
    intEnd = Intensity(table.get(str(end)), Ia,Ip,Kd,Ks,specIndex,L,V)

    # Compute change of intensity
    if(end[1] - start[1] == 0):
        dI = None
    else:
        # Remember ambient stays the same 
        tempy = (intEnd[1] - intStart[1])/(end[1]-start[1])
        tempz = (intEnd[2] - intStart[2])/(end[1]-start[1])
        dI = [0,tempy,tempz]

    # Get the average normals of (start,end)
    nStart = table.get(str(start))
    nEnd = table.get(str(end))

    # Compute change of normal
    if(end[1] - start[1] == 0):
        dN = None
    else:
        dN = [(nEnd[i] - nStart[i])/(end[1]-start[1]) for i in range(len(nEnd))]

    return intStart,intEnd,dI,nStart,nEnd,dN

    
# This function takes in a vertex surface normal,N, and applies the 
# illumination model to it to find its intensity
# Returns a list containing the components such: [ambient,diffuse,specular]
def Intensity(N,Ia,Ip,Kd,Ks,specIndex,L,V):
    # Find the reflection
    R = reflect(N,L)

    # Calculate ambient, diffuse, and specular
    amb = ambient(Ia,Kd)
    diff = diffuse(Ip,Kd,N,L)
    spec = specular(Ip,Ks,specIndex,R,V)

    # Return the vertex intensity components
    return [amb,diff,spec]


# This function takes in a polygon, zBuffer, and normal table, then applies the Gouraud Shading Algorithm
# by calculating intensities at the vertices, then performing a bi-linear interpolation of the intensities
def GouraudShade(poly,zBuffer,nTable):
    # Check if polygon is visible
    if(backFace(poly) == True):

        # Convert polygon vertices to display coordinates
        # Round the coordinates 
        displayPoly = [cTDC(project(vertex)) for vertex in poly]

        # Compute the fill table for the polygon
        edgeTable = fillTable(displayPoly,nTable)

        # List of the edges in order
        keys = [s for s in edgeTable.keys()]

        # Check if table is not empty
        if(bool(edgeTable) == True):

            # Smallest y value in table
            firstFillLine = edgeTable.get(keys[0])[1]
            
            # Create a temporary list with all yEnd values
            # Set the lastFillLine equal to the larget of the list
            tempList = [edgeTable.get(x)[2] for x in edgeTable.keys()]
            lastFillLine = max(tempList)


            # Indices for the first, second, and next edge
            I = 0
            J = 1
            Next = 2

            # Paint a fill LINE by selecting all picxels between two edges
            EdgeIX = edgeTable.get(keys[I])[0]
            EdgeJX = edgeTable.get(keys[J])[0]
            EdgeIZ = edgeTable.get(keys[I])[4]
            EdgeJZ = edgeTable.get(keys[J])[4]
            EdgeII = edgeTable.get(keys[I])[6] # intStart
            EdgeJI = edgeTable.get(keys[J])[7] # intEnd

            # Paint one fill line at a time
            for y in range(firstFillLine,lastFillLine+1):

                # Determine which edge is left and right
                if(EdgeIX < EdgeJX):
                    LeftX = EdgeIX
                    LeftZ = EdgeIZ
                    LeftI = EdgeII
                    RightX = EdgeJX
                    RightZ = EdgeJZ
                    RightI = EdgeJI
                    
                else:
                    LeftX = EdgeJX
                    LeftZ = EdgeJZ
                    LeftI = EdgeJI
                    RightX = EdgeIX
                    RightZ = EdgeIZ
                    RightI = EdgeII

                # Initial Z for current fill line
                z = LeftZ

                # Initial intensity
                i = LeftI

                # Compute dz for the fill line. Can be 0 if line is 1 pixel long
                if((RightZ - LeftZ) != 0):
                    dzFillLine = (RightZ - LeftZ)/(RightX - LeftX)
                else:
                    dzFillLine = 0

                # Compute dI for the fill line. Can be 0 if line is 1 pixel long
                if((RightX - LeftX) != 0):
                    dIFillLine = [(RightI[s] - LeftI[s])/(RightX - LeftX) for s in range(len(RightI))]
                else:
                    dIFillLine = [0,0,0]
                    
                # Paint a single pixel at a time
                for x in range(round(LeftX),round(RightX+1)):
                    # Check the pixel Zps for color priority
                    if(z < zBuffer[x][y]):
                        # Get the color of the pixel
                        color = triColorHexCode(i[0],i[1],i[2])
                        # Color the pixel
                        w.create_line(x,y,x+1,y,fill=color)
                        # Store that pixel ZpS
                        zBuffer[x][y] = z
                    # Update the new Zps
                    z += dzFillLine

                    # Update intensity for fill line
                    i = [i[s] + dIFillLine[s] for s in range(len(i))]
                    

                # Update the x and z values of edges I and J for the next fill line
                EdgeIX = EdgeIX + edgeTable.get(keys[I])[3]
                EdgeJX = EdgeJX + edgeTable.get(keys[J])[3]
                EdgeIZ += edgeTable.get(keys[I])[5]
                EdgeJZ += edgeTable.get(keys[J])[5]
                EdgeII = [EdgeII[s] + edgeTable.get(keys[I])[8][s] for s in range(len(EdgeII))] # Update the intensities for horizontal fill line
                EdgeJI = [EdgeJI[s] + edgeTable.get(keys[J])[8][s] for s in range(len(EdgeJI))] # Update the intensities for horizontal fill line

                # Upon reaching the bottom of an edge, switch out with next available
                if((y >= edgeTable.get(keys[I])[2]) and (y < lastFillLine)):
                    I = Next
                    EdgeIX = edgeTable.get(keys[I])[0]
                    EdgeIZ = edgeTable.get(keys[I])[4]
                    EdgeII = edgeTable.get(keys[I])[6] # intStart
                    Next +=1
                if((y >= edgeTable.get(keys[J])[2]) and (y < lastFillLine)):
                    J = Next
                    EdgeJX = edgeTable.get(keys[J])[0]
                    EdgeJZ = edgeTable.get(keys[J])[4]
                    EdgeJI = edgeTable.get(keys[J])[6] # intStart
                    Next +=1


# ************************************ Phong Shading **************************************
 # This function takes in a polygon, zBuffer, and normal table for all vertices
 # It calculates a fill/shade table based on that information
 # Afterwards it uses the approximate normals of vertices to perform a bi-linear interpolation of the normals
 # It computes a Phong Illumination Model on each pixel using its approximated normal, then paints with the correct color
def PhongShade(poly,zBuffer,nTable):
    # Check if polygon is visible
    if(backFace(poly) == True):

        # Convert polygon vertices to display coordinates
        # Round the coordinates 
        displayPoly = [cTDC(project(vertex)) for vertex in poly]

        # Compute the fill table for the polygon
        edgeTable = fillTable(displayPoly,nTable)

        # List of the edges in order
        keys = [s for s in edgeTable.keys()]

        # Check if table is not empty
        if(bool(edgeTable) == True):

            # Smallest y value in table
            firstFillLine = edgeTable.get(keys[0])[1]
            
            # Create a temporary list with all yEnd values
            # Set the lastFillLine equal to the larget of the list
            tempList = [edgeTable.get(x)[2] for x in edgeTable.keys()]
            lastFillLine = max(tempList)


            # Indices for the first, second, and next edge
            I = 0
            J = 1
            Next = 2

            # Paint a fill LINE by selecting all picxels between two edges
            EdgeIX = edgeTable.get(keys[I])[0]
            EdgeJX = edgeTable.get(keys[J])[0]
            EdgeIZ = edgeTable.get(keys[I])[4]
            EdgeJZ = edgeTable.get(keys[J])[4]
            EdgeIN = edgeTable.get(keys[I])[9] # nStart
            EdgeJN = edgeTable.get(keys[J])[10] # nEnd
            

            # Paint one fill line at a time
            for y in range(firstFillLine,lastFillLine+1):

                # Determine which edge is left and right
                if(EdgeIX < EdgeJX):
                    LeftX = EdgeIX
                    LeftZ = EdgeIZ
                    LeftN = EdgeIN
                    RightX = EdgeJX
                    RightZ = EdgeJZ
                    RightN = EdgeJN
                else:
                    LeftX = EdgeJX
                    LeftZ = EdgeJZ
                    LeftN = EdgeJN
                    RightX = EdgeIX
                    RightZ = EdgeIZ
                    RightN = EdgeIN

                # Initial Z for current fill line
                z = LeftZ

                # Initial N for current fill line
                n = LeftN

                # Compute dz for the fill line. Can be 0 if line is 1 pixel long
                if((RightZ - LeftZ) != 0):
                    dzFillLine = (RightZ - LeftZ)/(RightX - LeftX)
                else:
                    dzFillLine = 0

                # Compute dN for the fill line. Can be 0 if line is 1 pixel long
                if((RightX - LeftX) != 0):
                    dNFillLine = [(RightN[s] - LeftN[s])/(RightX - LeftX) for s in range(len(RightN))]
                else:
                    dNFillLine = [0,0,0]
                    
                    
                # Paint a single pixel at a time
                for x in range(round(LeftX),round(RightX+1)):
                    # Check the pixel Zps for color priority
                    if(z < zBuffer[x][y]):
                        
                        # Get the intensity components using the approximated normal for the pixel
                        i = Intensity(n,Ia,Ip,Kd,Ks,specIndex,L,V)
                        # Get the specific color for those specific components
                        color = triColorHexCode(i[0],i[1],i[2])

                        # Color the pixel
                        w.create_line(x,y,x+1,y,fill=color)
                        # Store that pixel ZpS
                        zBuffer[x][y] = z
                        
                    # Update the new Zps
                    z += dzFillLine

                    # Update the normal
                    n = [n[s] + dNFillLine[s] for s in range(len(n))]
                    

                # Update the x and z values of edges I and J for the next fill line
                EdgeIX = EdgeIX + edgeTable.get(keys[I])[3]
                EdgeJX = EdgeJX + edgeTable.get(keys[J])[3]
                EdgeIZ += edgeTable.get(keys[I])[5]
                EdgeJZ += edgeTable.get(keys[J])[5]
                EdgeIN = [EdgeIN[s] + edgeTable.get(keys[I])[11][s] for s in range(len(EdgeIN))] # Add the dN for the next horizontal fill line
                EdgeJN = [EdgeJN[s] + edgeTable.get(keys[J])[11][s] for s in range(len(EdgeJN))] # Add the dN for the next horizontal fill line

                # Upon reaching the bottom of an edge, switch out with next available
                if((y >= edgeTable.get(keys[I])[2]) and (y < lastFillLine)):
                    I = Next
                    EdgeIX = edgeTable.get(keys[I])[0]
                    EdgeIZ = edgeTable.get(keys[I])[4]
                    EdgeIN = edgeTable.get(keys[I])[9] # nStart
                    Next +=1
                if((y >= edgeTable.get(keys[J])[2]) and (y < lastFillLine)):
                    J = Next
                    EdgeJX = edgeTable.get(keys[J])[0]
                    EdgeJZ = edgeTable.get(keys[J])[4]
                    EdgeJN = edgeTable.get(keys[J])[9] # nStart
                    Next +=1
    




# *****************************************************************************************
# Everything below this point implements the interface
def reset():
    w.delete(ALL)
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    # If cylinder
    if(object == scene[0]):
        resetCylinder()
 
    createScene()
    

def larger():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cylinder
    if(object == scene[0]):
        scale(cylinderPointCloud,1.1)
       
    createScene()

def smaller():
    # Figuring out whic shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        scale(cylinderPointCloud,.9)
        
    createScene()
   

def forward():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(cylinderPointCloud,[0,0,5])
        
    createScene()
  

def backward():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(cylinderPointCloud,[0,0,-5])
    
    createScene()
  
def left():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(cylinderPointCloud,[-5,0,0])
       
    createScene()
  
def right():
    # Figuring out which shape is selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(cylinderPointCloud,[5,0,0])
        
    createScene()
  

def up():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(cylinderPointCloud,[0,5,0])
       
    createScene()

def down():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        translate(cylinderPointCloud,[0,-5,0])
        
    createScene()


def xPlus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateX(cylinderPointCloud,5)
        
    createScene()


def xMinus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateX(cylinderPointCloud,-5)
        
    createScene()

def yPlus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateY(cylinderPointCloud,5)
       
    createScene()

def yMinus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateY(cylinderPointCloud,-5)
        
    createScene()

def zPlus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateZ(cylinderPointCloud,5)
       
    createScene()

def zMinus():
    # Figuring out which shape the user selected
    global scene
    global selected
    object = scene[selected]
    w.delete(ALL)
    # If cube 1
    if(object == scene[0]):
        rotateZ(cylinderPointCloud,-5)
         
    createScene()

    
# Arrow key controls for <left>
def lKey(event):
    # Grabs the index of the current user selected shape
    global selected
    w.delete(ALL)
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
    w.delete(ALL)
    # If the shape is furtherest right, move to the furtherest left shape
    if(selected == 2):
        selected = 0
    # Otherwise, move to the next right shape
    else:
        selected += 1
    createScene()

# Key control for '1'
def oneKey(event):
    # Clear the scene
    w.delete(ALL)
    # Change the mode
    global mode
    mode = 1
    # Redraw the scene
    createScene()

# Key control for '2'
def twoKey(event):
    # Clear the screen
    w.delete(ALL)
    # Change the mode
    global mode
    mode = 2
    # Redraw the screen
    createScene()

# Key control for '3'
def threeKey(event):
    # Clear the screen
    w.delete(ALL)
    # Change the mode
    global mode
    mode = 3
    # Redraw the scene
    createScene()

# Key control for '4'
def fourKey(event):
    # Clear the screen
    w.delete(ALL)
    # Change the mode
    global mode
    mode = 4
    # Redraw the screen
    createScene()

# Key control for '5'
def fiveKey(event):
    # Clear the screen
    w.delete(ALL)
    # Change the mode
    global mode
    mode = 5
    # Redraw the screen
    createScene()

# Key control for '6'
def sixKey(event):
    # Clear the screen
    w.delete(ALL)
    # Change the mode
    global mode
    mode = 6
    # Redraw the scene
    createScene()


root = Tk()
# Create '<' and '>' key bindings w/ callback functions
#root.bind('<Left>',lKey)
#root.bind('<Right>', rKey)
# Create '1', '2','3', '4', '5', and '6' key bindings w/ callback functions
root.bind('1',oneKey)
root.bind('2',twoKey)
root.bind('3',threeKey)
root.bind('4',fourKey)
root.bind('5',fiveKey)
root.bind('6',sixKey)
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
scene = [cylinder]
# Automatically set the selected shape for the first image
selected = 0
# The drawing mode starts in mode 1 (wireframe)
mode = 1
# Generate the first image of objects
createScene()

# Launch the GUI
root.mainloop()







