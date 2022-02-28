import open3d as o3d

# pcd = o3d.io.read_point_cloud("~/3DModels/Octagon/real-octagon.ply")
# o3d.io.write_point_cloud("~/3DModels/Octagon/RealOct.pcd", pcd)

pcd = o3d.io.read_point_cloud("simplified-resized-real-octagon.ply")
o3d.io.write_point_cloud("SimplifiedResizedRealOctagon.pcd", pcd)

pcd = o3d.io.read_point_cloud("reconstructed-octagon.ply")
o3d.io.write_point_cloud("ReconstructedOctagon.pcd", pcd)