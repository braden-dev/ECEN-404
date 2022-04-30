from cv2 import split
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import math

# Reads the points from a .pcd file and then calculates the min and max x & y bounds
# and finds the min and max x & y values and also adds all the x,y,&z coords to their own lists
def readPCDFile(fileName):
    file = open(fileName, 'r')
    Lines = file.readlines()

    xCoord, yCoord, zCoord = [], [], []

    for line in Lines:
        # only continues if the value is a '-' or a number 
        # (based on the ASCII values of the digits 0 to 9)
        if(line[0] == '-' or (ord(line[0]) >= 48 and ord(line[0]) <= 57)):
            splitLine = line.split(" ")
            xCoord.append(float(splitLine[0]))
            yCoord.append(float(splitLine[1]))
            zCoord.append(float(splitLine[2]))

    file.close()

    maxX, minX, maxY, minY = max(xCoord), min(xCoord), max(yCoord), min(yCoord)

    deltaX = (maxX - minX)/10
    deltaY = (maxY - minY)/10

    minXBound, maxXBound, minYBound, maxYBound = (minX - deltaX), (maxX + deltaX), (minY - deltaY), (maxY + deltaY)
    return minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord

# Creates a density plot/histogram using the data from the original .pcd file
def createDensityPlot(minXBound, maxXBound, minYBound, maxYBound, xCoord, yCoord):
    xEdges = np.linspace(minXBound, maxXBound, 100)
    yEdges = np.linspace(minYBound, maxYBound, 100)

    xCoordArray = np.array(xCoord)
    yCoordArray = np.array(yCoord)

    h, xEdges, yEdges = np.histogram2d(xCoordArray,yCoordArray,bins=(xEdges, yEdges))
    h = h.T

    # Displays the colored density map with a color bar
    # plt.figure()
    # xx, yy = np.meshgrid(xEdges, yEdges)
    # plt.pcolormesh(xx, yy, h)
    # plt.colorbar()
    # plt.show()

    return h

# Calculates how many bins in the histogram
# have at least one point in them
def totalBinsFilled(h):
    densityMap = h.copy()
    numBinsFilled = 0
    for i in range(99):
        row = densityMap[i]
        for j in range(99):
            if(row[j] != 0):
                numBinsFilled += 1
    return numBinsFilled

# Reads the histogram and finds the location of the densest cluster of points
# then calculates all the distances of all the points from that spot
# and only adds the closest points to new lists which are used to make a new .pcd file
def findDensestPointDistancesandNewCoords(h, minX, maxX, minY, maxY, xCoord, yCoord, zCoord):
    densityMap = h.copy()
    max, densestRow, densestCol = 0, 0, 0
    for i in range(99):
        row = densityMap[i]
        for j in range(99):
            if(row[j] > max):
                max = row[j]
                densestRow = i
                densestCol = j

    # might be able to improve this coord, but good enough for now
    densestPointXCoord = minX + ((maxX - minX) * (densestCol/100))
    densestPointYCoord = minY + ((maxY - minY) * (densestRow/100))

    distFromDensestPoint = []

    sumDistances = 0
    for i in range(len(xCoord)):
        distFromDensestPoint.append(math.dist([densestPointXCoord, densestPointYCoord],[xCoord[i],yCoord[i]]))
        sumDistances += math.dist([densestPointXCoord, densestPointYCoord],[xCoord[i],yCoord[i]])

    avgDistanceFromDensestPoint = sumDistances / len(distFromDensestPoint) 

    croppedXCoords, croppedYCoords, croppedZCoords = [], [] ,[]

    # Only adds the coords of a point if the point's distance from the densest coords are less than the average distance
    for i in range(len(distFromDensestPoint)):
        if(distFromDensestPoint[i] <= avgDistanceFromDensestPoint):
            croppedXCoords.append(xCoord[i])
            croppedYCoords.append(yCoord[i])
            croppedZCoords.append(zCoord[i])

    return croppedXCoords, croppedYCoords, croppedZCoords

# Writes the new x,y,&z coords to a new .pcd file after removing all the far away points
def writeNewPCDFile(fileName, croppedXCoords, croppedYCoords, croppedZCoords):
    croppedPCDFile = open(fileName, "w")
    intro = f"# .PCD v0.7 - Point Cloud Data file format\nVERSION 0.7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH {len(croppedXCoords)}\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS {len(croppedXCoords)}\nDATA ascii\n"
    croppedPCDFile.write(intro)

    for i in range(len(croppedXCoords)):
        stringOfCoords = f"{croppedXCoords[i]} {croppedYCoords[i]} {croppedZCoords[i]}\n"
        croppedPCDFile.write(stringOfCoords)


def runCroppingProcess():
    # Runs the process twice to remove as many unnecessary points as possible (uses transformed point cloud starting out)
    # minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile("TransformedOutputPointCloud.pcd")
    # Uses non-transformed point cloud starting out
    minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile("OutputPointCloud.pcd")
    h = createDensityPlot(minXBound, maxXBound, minYBound, maxYBound, xCoord, yCoord)
    croppedXCoords, croppedYCoords, croppedZCoords = findDensestPointDistancesandNewCoords(h, minX, maxX, minY, maxY, xCoord, yCoord, zCoord)
    writeNewPCDFile("CroppedPCDOutputFile.pcd", croppedXCoords, croppedYCoords, croppedZCoords)

    minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile("CroppedPCDOutputFile.pcd")
    h = createDensityPlot(minXBound, maxXBound, minYBound, maxYBound, xCoord, yCoord)
    croppedXCoords, croppedYCoords, croppedZCoords = findDensestPointDistancesandNewCoords(h, minX, maxX, minY, maxY, xCoord, yCoord, zCoord)
    writeNewPCDFile("Cropped2PCDOutputFile.pcd", croppedXCoords, croppedYCoords, croppedZCoords)

    minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile("Cropped2PCDOutputFile.pcd")
    h = createDensityPlot(minXBound, maxXBound, minYBound, maxYBound, xCoord, yCoord)
    croppedXCoords, croppedYCoords, croppedZCoords = findDensestPointDistancesandNewCoords(h, minX, maxX, minY, maxY, xCoord, yCoord, zCoord)
    writeNewPCDFile("Cropped3PCDOutputFile.pcd", croppedXCoords, croppedYCoords, croppedZCoords)

    # minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile("Cropped3PCDOutputFile.pcd")
    # h = createDensityPlot(minXBound, maxXBound, minYBound, maxYBound, xCoord, yCoord)
    # croppedXCoords, croppedYCoords, croppedZCoords = findDensestPointDistancesandNewCoords(h, minX, maxX, minY, maxY, xCoord, yCoord, zCoord)
    # writeNewPCDFile("Cropped4PCDOutputFile.pcd", croppedXCoords, croppedYCoords, croppedZCoords)

def scalePCD(pcd, factor):
    minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile(pcd)
    scaledX, scaledY, scaledZ = [], [], []
    for i in range(len(xCoord)):
        scaledX.append(xCoord[i] * factor)
    for j in range(len(yCoord)):
        scaledY.append(yCoord[j] * factor)
    for k in range(len(zCoord)):
        scaledZ.append(zCoord[k] * factor)
    scaledPCD = "Scaled" + pcd
    writeNewPCDFile(scaledPCD, scaledX, scaledY, scaledZ)