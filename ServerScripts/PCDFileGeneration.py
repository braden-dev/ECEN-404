import numpy as np
from scipy.spatial.transform import Rotation
import open3d as o3d
from PCDFileParser import *

#temporary
from ModelComparisonCoreFunctions import *

print("Generating PCD File...")
# Actual PCD Generation 
pcd = o3d.io.read_point_cloud("scene_dense_mesh_refine.ply")
o3d.io.write_point_cloud("OutputPointCloud.pcd", pcd, write_ascii=True)
print("Generated PCD File Successfully.")

# Transform the point cloud to the position in the real world
# outputPointCloud = o3d.io.read_point_cloud("OutputPointCloud.pcd")

# Pseudocode:
# 1) rotation in Euler angles
# 2) convert that into an array where the last column is all 0s bc I don't need to translate it
# 3) transform the point cloud by that transformation array
# 4) write that to another (or the same) PCD file


# initTransformEuler = [-154,22.2,0]
# bestInitEulerTransform = [-137,-3,0]
# bestInitEulerTransform = [-154,12,0]


# Process trying to find the best orientation

# start = time.time()

# absMaxXBound, absMinXBound, absMaxYBound, absMinYBound = 0, 0, 0, 0

# for x in range (-170,-120,4):
#     for y in range(-20,20,4):
#         initTransformEuler = [x,y,0]
#         initTransformMatrix = Rotation.from_euler('xyz',initTransformEuler,degrees=True).as_matrix()
#         addRow = np.array([[0.0,0.0,0.0]])
#         initCompleteTransformMatrix = np.r_[initTransformMatrix,addRow]
#         addCol = np.array([[0.0],[0.0],[0.0],[1.0]])
#         initCompleteTransformMatrix = np.c_[initCompleteTransformMatrix,addCol]
#         o3d.io.write_point_cloud("TransformedOutputPointCloud.pcd", outputPointCloud.transform(initCompleteTransformMatrix), write_ascii=True)
#         minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile("TransformedOutputPointCloud.pcd")

#         if(minXBound < absMinXBound):
#             absMinXBound = minXBound

#         if(minYBound < absMinYBound):
#             absMinYBound = minYBound

#         if(maxXBound > absMaxXBound):
#             absMaxXBound = maxXBound

#         if(maxYBound > absMaxYBound):
#             absMaxYBound = maxYBound

# # startingTransform = [0,0,0]
# # initTransformMatrix = Rotation.from_euler('xyz',startingTransform,degrees=True).as_matrix()
# # addRow = np.array([[0.0,0.0,0.0]])
# # initCompleteTransformMatrix = np.r_[initTransformMatrix,addRow]
# # addCol = np.array([[0.0],[0.0],[0.0],[1.0]])
# # initCompleteTransformMatrix = np.c_[initCompleteTransformMatrix,addCol]
# # o3d.io.write_point_cloud("TransformedOutputPointCloud.pcd", outputPointCloud.transform(initCompleteTransformMatrix), write_ascii=True)
# # constantMinXBound, constantMaxXBound, constantMinYBound, constantMaxYBound, constantMaxX, constantMinX, constantMaxY, constantMinY, constantxCoord, constantyCoord, constantzCoord = readPCDFile("TransformedOutputPointCloud.pcd")


# initTransformEuler = [0,0,0]
# binsFilled = 0
# bestX, bestY, bestZ = 0,0,0
# for x in range (-170,-120,4):
#     for y in range(-20,20,4):
#         # for z in range(-180,180,20):
#         initTransformEuler = [x,y,0]
#         initTransformMatrix = Rotation.from_euler('xyz',initTransformEuler,degrees=True).as_matrix()
#         addRow = np.array([[0.0,0.0,0.0]])
#         initCompleteTransformMatrix = np.r_[initTransformMatrix,addRow]
#         addCol = np.array([[0.0],[0.0],[0.0],[1.0]])
#         initCompleteTransformMatrix = np.c_[initCompleteTransformMatrix,addCol]
#         o3d.io.write_point_cloud("TransformedOutputPointCloud.pcd", outputPointCloud.transform(initCompleteTransformMatrix), write_ascii=True)
#         minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile("TransformedOutputPointCloud.pcd")
#         h = createDensityPlot(absMinXBound, absMaxXBound, absMinYBound, absMaxYBound, xCoord, yCoord)
#         if(totalBinsFilled(h) > binsFilled):
#             binsFilled = totalBinsFilled(h)
#             print(binsFilled)
#             bestX, bestY, bestZ = x, y, 0

# bestInitEulerTransform = [bestX, bestY, bestZ]
# print(bestInitEulerTransform)

# print("Total time was %.3f sec." % (time.time() - start))

# End process

# initTransformMatrix = Rotation.from_euler('xyz',bestInitEulerTransform,degrees=True).as_matrix()
# # print(initTransformMatrix)

# addRow = np.array([[0.0,0.0,0.0]])
# initCompleteTransformMatrix = np.r_[initTransformMatrix,addRow]
# addCol = np.array([[0.0],[0.0],[0.0],[1.0]])
# initCompleteTransformMatrix = np.c_[initCompleteTransformMatrix,addCol]
# # print(initCompleteTransformMatrix)

# o3d.io.write_point_cloud("TransformedOutputPointCloud.pcd", outputPointCloud.transform(initCompleteTransformMatrix), write_ascii=True)

# minXBound, maxXBound, minYBound, maxYBound, maxX, minX, maxY, minY, xCoord, yCoord, zCoord = readPCDFile("TransformedOutputPointCloud.pcd")
# h = createDensityPlot(minXBound, maxXBound, minYBound, maxYBound, xCoord, yCoord)
# print(totalBinsFilled(h))