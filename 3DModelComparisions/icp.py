import open3d as o3d

# pcd = o3d.io.read_point_cloud("~/3DModels/Octagon/real-octagon.ply")
# o3d.io.write_point_cloud("~/3DModels/Octagon/RealOct.pcd", pcd)

# pcd = o3d.io.read_point_cloud("simplified-real-octagon02-centered.ply")
# o3d.io.write_point_cloud("SimplifiedResizedCenteredRealOctagon.pcd", pcd)

# pcd = o3d.io.read_point_cloud("SAMPLE-TARGET-reconstructed-octagon-centered.ply")
# o3d.io.write_point_cloud("SampleOctagonTarget.pcd", pcd)

# pcd = o3d.io.read_point_cloud("reconstructed-octagon-centered.ply")
# o3d.io.write_point_cloud("ReconstructedCenteredOctagon.pcd", pcd)

pcd = o3d.io.read_point_cloud("closeup-scene-source-test02-hololens.ply")
o3d.io.write_point_cloud("closeup-scene-source-test02-hololens.pcd", pcd)

# pcd = o3d.io.read_point_cloud("BEST-reconstruction-edited.ply")
# o3d.io.write_point_cloud("TargetOctagon.pcd", pcd)