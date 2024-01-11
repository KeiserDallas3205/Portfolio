##################################################
# Name: Keiser Dallas
# Date: 2/6/2023
# Demo: Computer Graphics -> 20 Spheres
#           - This is an implementation of the 20 spheres demo to the use of illumination models
#               to alter one sphere's appearance 20 times
###################################################

from math import *
from tkinter import *

# Given constants for demo
Ia = .3
Ip = .7
L = [1,1,1]
V = [0,0,1]

# This function normalizes any given vector
# Returns its corresponding unit vector
def norm(vector):
    vNorm = [(x/magnitude(vector)) for x in vector]
    return vNorm

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

# Calculate a 3D reflection vector, R, given surface normal, N, and lighting vector, L
def reflect(N,L):
    R = []
    N = norm(N)
    L = norm(L)
    twoCosPhi = 2 * dot(N,L)

    if(twoCosPhi > 0):
        for i in range(3):
            R.append(N[i] - (L[i] / twoCosPhi))
    elif(twoCosPhi == 0):
        for i in range(3):
            R.append(-L[i])
    else:
        for i in range(3):
            R.append(-N[i] + (L[i] / twoCosPhi))

    return norm(R)

# This function creates the screen display by taken in all given constants
# Takes in ambient intensity, point light intensity, lighting vector, and view vector
def render20Spheres(Ia,Ip,L,V):
    # Sphere characteristics
    xCenter = 150 # x center of first sphere on each row
    yCenter = 112 # y center of first sphere on FIRST row
    radius = 50
    specIndex = [2,4,8,16] # specIndex for all rows in order
    Kd = 0 # kd of first sphere of each row
    Ks = 1 # ks of first sphere of each row
    
    # There will be four rows of spheres
    for row in range(4):
        # There will be five spheres per row
        for col in range(5):
            # Paint a sphere
            renderSphere(xCenter,yCenter,radius,Kd,Ks,specIndex[row],Ia,Ip,L,V)

            # Prep for next sphere on row
            Kd += .25
            Ks -= .25
            xCenter += 125

        # Prep for next row of spheres
        xCenter = 150 # Reset xCenter
        yCenter += 125 # Increment yCenter for next row
        Kd = 0 # Reset Kd
        Ks = 1 # Reset Ks


# This function renders one individual sphere, given its xCenter, yCenter, radius,
# Kd, Ks, specIndex, Ia, Ip, L, V
def renderSphere(xCenter,yCenter,radius,Kd,Ks,specIndex,Ia,Ip,L,V):
    L = norm(L)
    V = norm(V)

    # Ambient diffuse component of illumination model
    ambient = Ia * Kd

    # Render a sphere
    rSquare = radius**2
    for y in range(-radius,radius+1):
        ySquare = y**2
        for x in range(-radius,radius+1):
            xSquare = x**2
            if((xSquare + ySquare) <= rSquare):
                z = round(sqrt(rSquare - xSquare - ySquare))
                N = norm([x,y,z])
                if(dot(N,L) < 0):
                    diffuse = 0
                else:
                    diffuse = Ip * Kd * dot(N,L)
                R = norm(reflect(N,L))
                if(dot(R,V) < 0):
                    specular = 0
                else:
                    specular = Ip * Ks * ((dot(R,V))**specIndex)
                # Set color of pixel
                color = triColorHexCode(ambient,diffuse,specular)
                # Draw the pixel
                w.create_line(xCenter+x,yCenter-y,xCenter+x+1,yCenter-y,fill=color)

# Generate a color hex code string from the illumination components
def triColorHexCode(ambient,diffuse,specular):
    combinedColorCode = colorHexCode(ambient + diffuse + specular)
    specularColorCode = colorHexCode(specular)
    colorString = '#' + specularColorCode + combinedColorCode + specularColorCode
    return colorString


# Helper function that checks the formatting of color code
def colorHexCode(intensity):
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
        





# Setup Tkinter GUI
CanvasWidth = 800
CanvasHeight = 600
root = Tk()
outerframe = Frame(root)
outerframe.pack()
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
render20Spheres(Ia,Ip,L,V)
w.pack()
root.mainloop()
