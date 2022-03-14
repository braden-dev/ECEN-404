import open3d as o3d

# pcd = o3d.io.read_point_cloud("~/3DModels/Octagon/real-octagon.ply")
# o3d.io.write_point_cloud("~/3DModels/Octagon/RealOct.pcd", pcd)

# pcd = o3d.io.read_point_cloud("simplified-real-octagon02-centered.ply")
# o3d.io.write_point_cloud("SimplifiedResizedCenteredRealOctagon.pcd", pcd)

# pcd = o3d.io.read_point_cloud("SAMPLE-TARGET-reconstructed-octagon-centered.ply")
# o3d.io.write_point_cloud("SampleOctagonTarget.pcd", pcd)

# pcd = o3d.io.read_point_cloud("reconstructed-octagon-centered.ply")
# o3d.io.write_point_cloud("ReconstructedCenteredOctagon.pcd", pcd)

# pcd = o3d.io.read_point_cloud("closeup-scene-source-test03-hololens.ply")
# o3d.io.write_point_cloud("closeup-scene-source-test03-hololens.pcd", pcd)

# pcd = o3d.io.read_point_cloud("BEST-reconstruction-edited-realpos01.ply")
# o3d.io.write_point_cloud("TargetOctagonRealPos01.pcd", pcd)

pcd = o3d.io.read_point_cloud("ASCII_RESIZED_reconstructed_viking_rover.ply")
o3d.io.write_point_cloud("rover_recon_test01.pcd", pcd)

pcd = o3d.io.read_point_cloud("ASCII_RESIZED_SIMPLIFIED_full_viking_rover.ply")
o3d.io.write_point_cloud("rover_predef_test01.pcd", pcd)