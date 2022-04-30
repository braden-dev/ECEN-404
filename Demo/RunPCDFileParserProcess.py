from PCDFileParser import *
import open3d as o3d

print("Cropping the PCD File...")
runCroppingProcess()
print("Finished Cropping the PCD File.")

# pcd = o3d.io.read_point_cloud("BEST-right-size-reconstruction-edited-realpos01.ply")
# o3d.io.write_point_cloud("BEST-right-size-reconstruction-edited-realpos01.pcd", pcd, write_ascii=True)

# pcd = o3d.io.read_point_cloud("Cropped2PCDOutputFile.pcd")
# o3d.io.write_point_cloud("Cropped2PCDOutputFile.ply", pcd)