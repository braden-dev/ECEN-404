from asyncio.windows_events import NULL


file = open('scene_dense_mesh_refine_texture.obj', 'r')
Lines = file.readlines()

count = 0
xCoord = []
yCoord = []
zCoord = []
allCoords = [[]]
for line in Lines:
    if(len(line) >= 2):
        if((line[0] == 'v') & (line[1] == ' ')):
            count += 1

            splitLine = line.split(" ")
            # print(splitLine)
            # if(count == 100):
            #     break
            xCoord.append(splitLine[1])
            yCoord.append(splitLine[2])
            zCoord.append(splitLine[3].split("\n")[0])

            #print(line)

file.close()

allCoords.append(xCoord)
allCoords.append(yCoord)
allCoords.append(zCoord)

# print(f"List of x coords: {xCoord}")
# print(f"List of y coords: {yCoord}")
# print(f"List of z coords: {zCoord}")
print(f"Length of x coords: {len(xCoord)}")
print(f"Length of y coords: {len(yCoord)}")
print(f"Length of z coords: {len(zCoord)}")
print(f"Num of lines: {count}")

file1 = open('full_viking_rover.obj', 'r')
Lines1 = file1.readlines()

count1 = 0
xCoord1 = []
yCoord1 = []
zCoord1 = []
allCoords1 = [[]]
for line in Lines1:
    if(len(line) >= 2):
        if((line[0] == 'v') & (line[1] == ' ')):
            count1 += 1

            splitLine = line.split(" ")
            # print(splitLine)
            # if(count == 100):
            #     break
            xCoord1.append(splitLine[1])
            yCoord1.append(splitLine[2])
            zCoord1.append(splitLine[3].split("\n")[0])

            #print(line)

file1.close()

allCoords1.append(xCoord1)
allCoords1.append(yCoord1)
allCoords1.append(zCoord1)

print(f"Length of x coords: {len(xCoord1)}")
print(f"Length of y coords: {len(yCoord1)}")
print(f"Length of z coords: {len(zCoord1)}")
print(f"Num of lines: {count1}")