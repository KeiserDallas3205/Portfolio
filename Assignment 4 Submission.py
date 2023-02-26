######################################
# Name: Keiser Dallas
# Date: 2/21/2023
# CSC 470-001
# Assignment 4: 
#
#
######################################
from tkinter import *
from math import *
from operator import itemgetter

#*********************** Scene Implementation **************************************

# Spheres have a center point, radius, RGB color, Kd, Ks, and specIndex
redSphere = [[300,-100,300],200,[1,0.5,0.5],0.5,0.5,8]
greenSphere = [[-300,-200,300], 100, [0.5,0.5,1],0.5,0.5,8]
blueSphere = [[0,0,800],300,[0.5,1,0.5],0.5,0.5,8]

# Checkerboard has a surface normal, anchor point, Kd, Ks, and specIndex
board = [[0,1,0], [0,-300,0], [0.5,0.5,1], 0.6, 0.4, 8]

# Collecton of objects to be drawn
scene = [board,redSphere,greenSphere,blueSphere]


# Function creates the image by driving the traceRay() method for each pixel in the canvas 
def renderImage():
    global L
    global illuminationSaturationCounter
    illuminationSaturationCounter = 0 
    L = norm(L)
    top = round(CanvasHeight/2)
    bottom = round(-CanvasHeight/2)
    left = round(-CanvasWidth/2)
    right = round(CanvasWidth/2)
    for y in range(top,bottom,-1):
        for x in range(left,right):
            # Compute initial ray
            ray = vector(centerOfProjection,[x,y,0])
            # Compute color
            color = traceRay(centerOfProjection,ray,4)
            # Paint the pixel
            w.create_line(right+x,top-y,right+x+1,top-y,fill=RGBColorHexCode(color))
    overSat = illuminationSaturationCounter / (CanvasWidth*CanvasHeight) * 100
    
    

#********************* Constants **************************************************
centerOfProjection = [0,0,-500]
Ia = .3
Ip = .7
L = [1,1,-1]
lightSource = [500,500,0]
V = [0,0,1]
illuminationSaturationCounter = 0
skyBoxColor = [0.53,0.81,0.92] # Blue
horizon = 1500

#********************* Ray Trace Methods ******************************************

# This function recursively traces where rays intersect with other objects from depth 4-1
# Computes a local color, reflected ray, and reflected color
# DOES NOT compute refracted ray or color
# Returns a combine color and weight 
def traceRay(startPoint,ray,depth):

    # Return 'black' when reaching maximum depth
    if(depth == 0):
        return [0,0,0]
    # Find the closest intersection
    nearest = [] # Array holds all intersection points
    table = {} # Dictionary to map an object -> intersection point
    # Checks for intersection points and only adds valid ones
    for object in scene:
        if(object == board):
            temp = intersectPlane(object,startPoint,ray)
            if(temp != [] and temp[2] > 0 and temp[2] < horizon): 
                nearest.append(temp)
                table[str(object)] = temp
        else:
            temp = intersectSphere(object,startPoint,ray)
            if(temp != [] and temp[2] > 0 and temp[2] < horizon):
                nearest.append(temp)
                table[str(object)] = temp
    # If there are no intersections, return skybox color
    if(nearest == []):
        return skyBoxColor
    else:
        
        # Sorts the list by the intersection point with the closest z value (nearest object)
        nearest = sorted(nearest,key=itemgetter(2))
        # Selects the first intersection point
        intersection = nearest[0]
        # Grab the corresponding object
        nearestObject = list(filter(lambda x: table[x] == intersection, table))[0]
        for object in scene:
            if(str(object) == nearestObject):
                nearestObject = object 
        
        # Grab the color of nearest object
        color = nearestObject[2]

        # Perform a Phong Illumination model on the object to determine intensities
        if(nearestObject == board):
            intensity = boardInt(intersection,nearestObject) # Get checkboard color at that pixel
            if(inShadow(nearestObject,intersection)):
                intensity = [intensity[i] * 0.25 for i in range(len(intensity))]
        else:
            n = [intersection[i] - nearestObject[0][i] for i in range(len(intersection))]# Calculate the normal at that point on sphere
            intensity = sphereInt(depth,ray,intersection,n,nearestObject) # Get the color of sphere at that point
            if(inShadow(nearestObject,intersection)):
                intensity = [intensity[i] * 0.25 for i in range(len(intensity))]

        # Compute the local color
        localColor = [color[i]*intensity[i]*2 for i in range(len(color))]
        localWeight = 0.5
        
        
        # Combine the local and reflected color
        combinedColor = [localColor[i] for i in range(len(localColor))]
        #combinedColor = [(localColor[i] * localWeight) + (reflectedColor[i] * reflectedWeight) for i in range(len(localColor))]
        return combinedColor

# This function takes in an object(sphere), starting point, and a ray
# Then checks if the ray interesects with a sphere 
# Returns an intersection point [x,y,z]
def intersectSphere(object,startPoint,ray):
    # Define the variables for quadratic
    a = sum([ray[s]**2 for s in range(len(ray))])
    b = 2 * ray[0] * (startPoint[0] - object[0][0]) + 2 * ray[1] * (startPoint[1] - object[0][1]) + 2 * ray[2] * (startPoint[2] - object[0][2])
    c = object[0][0]**2 + object[0][1]**2 + object[0][2]**2 + startPoint[0]**2 + startPoint[1]**2 + startPoint[2]**2 + 2 * (-object[0][0] * startPoint[0] - object[0][1] * startPoint[1] - object[0][2] * startPoint[2]) - object[1]**2

    # Check the discriminant
    discriminant = (b**2) - 4 * a * c
    if(discriminant < 0):
        t = None # No real roots, no intersection
    elif(discriminant > 0):
        # Two real roots, and two intersection points
        # Calculate both roots and choose the smaller one 
        t1 = (-b + sqrt(discriminant))/(2*a)
        t2 = (-b - sqrt(discriminant))/(2*a)
        t = min(t1,t2)
    else: #(discriminant == 0)
        # One real root, one intersection point
        t = -b/(2*a)

    # Plug t in to find intersection point
    if(t == None):
        return []
    else:
        intersection = [(startPoint[i] + ray[i] * t) for i in range(len(ray))]

    return intersection

# This function takes in an object(plane), starting point, and a ray
# Then checks if the ray intersects the plane
# Returns an intersection point [x,y,z]
def intersectPlane(object,startPoint,ray):
    # Check the denominator of the t equation
    denominator = dot(object[0],ray)
    if(denominator == 0):
        t = None # No real root, no intersection point
    else: # One real root, one intersection
        # Calculate D
        D = dot(object[0],object[1])
        # Calculate t
        t = -(object[0][0] * startPoint[0] + object[0][1] * startPoint[1] + object[0][2] * startPoint[2] - D)/denominator

    if(t == None or t < 0):
        intersection = []
    else:
        intersection = [(startPoint[s] + ray[s] * t) for s in range(len(ray))]

    return intersection

# This is the reflection equation used for TRACED RAYS
# Calculate a 3D reflection vector, R, given the surface normal of intersection point and traced ray vector
# Returns a vector [x,y,z]
def reflect(N,T):
    R = []
    N = norm(N)
    T = norm(T)
    negT = norm([-T[i] for i in range(len(T))])
    twoCosPhi = 2 * dot(N,negT)

    if(twoCosPhi > 0): 
        R = [(N[i] + (T[i]/(2*dot(N,negT)))) for i in range(len(N))]
    elif(twoCosPhi == 0):
        R = [T[i] for i in range(len(T))]
        
    return norm(R)

#************************* Phong Intensities **************************************
# This function takes in a point [X,Y,Z] 
# Then it computes the new intensity of those colors
# Returns a color [R,G,B]
def boardInt(point,object):
    
    outOfBounds = False
    # Checks left/right positioning on board
    if(point[0] >= 0):
        colorFlag = True # Red
    else:
        colorFlag = False # White

    # Checks vertical positioning on board
    if(abs(point[0])%200 > 100):
        colorFlag = not colorFlag
    if(abs(point[2])%200 > 100):
        colorFlag = not colorFlag
    if(point[2] > horizon):
        outOfBounds = True

    if(outOfBounds):
        return skyBoxColor
    # Returns the new color
    elif(colorFlag):
        color = [1,0,0] # Red
    else:
        color = [1,1,1] # White

    return color
    
    
    
# This function takes in a level(depth), ray <i,j,k>, point [X,Y,Z], normal [X,Y,Z], and color [R,G,B]
# Then it computes the intensity of those colors using Phong illumination model
# Returns a new color [R,G,B]
def sphereInt(level,ray,point,n,object):
    # Normalize the ray and the normal
    ray = norm(ray)
    n = norm(n)

    # Calculate the reflection
    r = reflect(n,ray)

    # Color of reflected ray
    color = traceRay(point,r,level-1)

    # Phong Illumination on ray
    intensity = PhongInt(n,object[3],object[4],object[5])

    # Add effects
    color = [color[i] * intensity[i] for i in range(len(color))]

    return color

# This function takes in interesection point's surface normal,N, constant of diffuse,
# constant of specular, and specIndex for the intersected object,and applies
# the Phong illumination model to it to find its intensity
# Returns a list of intensities [R,G,B]
def PhongInt(N,Kd,Ks,specIndex):
    global Ia
    global Ip
    global L
    global V
    # Find the reflection
    R = reflectPhong(N,L)

    # Calculate ambient
    ambient = Ia * Kd
    
    # Calculate diffuse
    if(dot(N,L) < 0):
        diffuse = 0
    else:
        diffuse =  Ip * Kd * dot(N,L)
        
    # Calculate specular 
    if(dot(R,V) < 0):
        specular =  0
    else:
        specular = Ip * Ks * ((dot(R,V))**specIndex)

    intensity = ambient + diffuse + specular
    return [intensity,intensity,intensity]

# This is the reflection equation used for PHONG ILLUMINATION MODEL
# Calculate a 3D reflection vector, R, given surface normal, N, and lighting vector, L
# Retuns a vector [x,y,z]
def reflectPhong(N,L):
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

def inShadow(startObject,startPoint):
    dim = False
    ray = vector(startPoint,lightSource)
    for object in scene:
        if(startObject != object):
            if(object == board):
                if(intersectPlane(object,startPoint,ray) != []):
                    dim = True
            else:
                if(intersectSphere(object,startPoint,ray) != []):
                    dim = True
    return dim
                    

#************************* Helper Functions ***************************************
# This function takes two points(start,end)
# Returns a vector (end - start)
def vector(start,end):
    v = []
    v = [z-x for x,z in zip(start,end)]
    return v 

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



# Function takes in intensities for red, green, and blue [ir,ig,ib]
# Then returns a color string
def RGBColorHexCode(color):
    colorString = '#'
    for intensity in color:
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
        colorString += trimmedHexString
    return colorString 

#********************* Canvas Setup ***********************************************

# Setup Tkinter GUI
CanvasWidth = 800
CanvasHeight = 600
root = Tk()
outerframe = Frame(root)
outerframe.pack()
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
renderImage() # Display
w.pack()
root.mainloop()




