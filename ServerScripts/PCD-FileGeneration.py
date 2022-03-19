import numpy as np
from scipy.spatial.transform import Rotation
import open3d as o3d

#temporary
from ModelComparisonCoreFunctions import *

# Actual PCD Generation 
pcd = o3d.io.read_point_cloud("scene_dense_mesh_refine.ply")
o3d.io.write_point_cloud("OutputPointCloud.pcd", pcd, write_ascii=True)

# Transform the point cloud to the position in the real world
outputPointCloud = o3d.io.read_point_cloud("OutputPointCloud.pcd")

# Pseudocode:
# 1) rotation in Euler angles
# 2) convert that into an array where the last column is all 0s bc I don't need to translate it
# 3) transform the point cloud by that transformation array
# 4) write that to another (or the same) PCD file

initTransformEuler = [-154,22.2,0]
initTransformMatrix = Rotation.from_euler('xyz',initTransformEuler,degrees=True).as_matrix()
# print(initTransformMatrix)

addRow = np.array([[0.0,0.0,0.0]])
initCompleteTransformMatrix = np.r_[initTransformMatrix,addRow]
addCol = np.array([[0.0],[0.0],[0.0],[1.0]])
initCompleteTransformMatrix = np.c_[initCompleteTransformMatrix,addCol]
# print(initCompleteTransformMatrix)

o3d.io.write_point_cloud("TransformedOutputPointCloud.pcd", outputPointCloud.transform(initCompleteTransformMatrix), write_ascii=True)