from cv2 import split
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import math


# file = open('OutputPointCloud.pcd', 'r')
file = open('TransformedOutputPointCloud.pcd', 'r')
Lines = file.readlines()

count = 0
xCoord, yCoord, zCoord = [], [], []
for line in Lines:
    # only continues if the value is a '-' or a number 
    # (based on the ASCII values of the digits 0 to 9)
    if(line[0] == '-' or (ord(line[0]) >= 48 and ord(line[0]) <= 57)):
        # count += 1

        splitLine = line.split(" ")
        xCoord.append(float(splitLine[0]))
        yCoord.append(float(splitLine[1]))
        zCoord.append(float(splitLine[2]))


file.close()

# print(f"List of x coords: {xCoord}")
# print(f"List of y coords: {yCoord}")

# print(f"Length of x coords: {len(xCoord)}")
# print(f"Length of y coords: {len(yCoord)}")

maxX, minX, maxY, minY = max(xCoord), min(xCoord), max(yCoord), min(yCoord)

deltaX = (maxX - minX)/10
deltaY = (maxY - minY)/10

# print(maxX, minX, maxY, minY)
# print(xCoord)

minXBound, maxXBound, minYBound, maxYBound = (minX - deltaX), (maxX + deltaX), (minY - deltaY), (maxY + deltaY)

plt.figure()
xEdges = np.linspace(minXBound, maxXBound, 100)
yEdges = np.linspace(minYBound, maxYBound, 100)
xx, yy = np.meshgrid(xEdges, yEdges)

xCoordArray = np.array(xCoord)
yCoordArray = np.array(yCoord)

h, xEdges, yEdges = np.histogram2d(xCoordArray,yCoordArray,bins=(xEdges, yEdges))
h = h.T
# print(h[98])
plt.pcolormesh(xx, yy, h)
plt.colorbar()
# plt.show()

densityMap = h.copy()
max, densestRow, densestCol = 0, 0, 0
for i in range(99):
    row = densityMap[i]
    for j in range(99):
        if(row[j] > max):
            max = row[j]
            densestRow = i
            densestCol = j

# print(max, densestCol, densestRow)

# might be able to improve this coord, but good enough for now
densestPointXCoord = minX + ((maxX - minX) * (densestCol/100))
densestPointYCoord = minY + ((maxY - minY) * (densestRow/100))

# print((maxX + minX), (maxY + minY))
# print(densestPointXCoord, densestPointYCoord)

distFromDensestPoint = []

sumDistances = 0
for i in range(len(xCoord)):
    distFromDensestPoint.append(math.dist([densestPointXCoord, densestPointYCoord],[xCoord[i],yCoord[i]]))
    sumDistances += math.dist([densestPointXCoord, densestPointYCoord],[xCoord[i],yCoord[i]])

avgDistanceFromDensestPoint = sumDistances / len(distFromDensestPoint) 

croppedXCoords, croppedYCoords, croppedZCoords = [], [] ,[]

for i in range(len(distFromDensestPoint)):
    if(distFromDensestPoint[i] <= avgDistanceFromDensestPoint):
        croppedXCoords.append(xCoord[i])
        croppedYCoords.append(yCoord[i])
        croppedZCoords.append(zCoord[i])

croppedPCDFile = open("CroppedPCDOutputFile.pcd", "w")
intro = f"# .PCD v0.7 - Point Cloud Data file format\nVERSION 0.7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH {len(croppedXCoords)}\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS {len(croppedXCoords)}\nDATA ascii\n"
croppedPCDFile.write(intro)

for i in range(len(croppedXCoords)):
    stringOfCoords = f"{croppedXCoords[i]} {croppedYCoords[i]} {croppedZCoords[i]}\n"
    croppedPCDFile.write(stringOfCoords)

plt.show()

# print(f"Max x coord: {maxX}")
# print(f"Min x coord: {minX}")
# print(f"Max y coord: {maxY}")
# print(f"Min y coord: {minY}")

# print(f"Num of lines: {count}")