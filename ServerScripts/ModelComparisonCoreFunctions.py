from cv2 import threshold
from matplotlib.pyplot import draw
import open3d as o3d
import numpy as np
import copy
from scipy.spatial.transform import Rotation

voxel_size = 10  # octagon
# voxel_size = 7  # rover (test01)
# voxel_size = 4  # rover (initial)

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4559,
                                      front=[0.6452, -0.3036, -0.7011],
                                      lookat=[1.9892, 2.0208, 1.8945],
                                      up=[-0.2779, -0.9482, 0.1556])


def preprocess_point_cloud(pcd, voxel_size):
    # print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    # print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    pcd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    # print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

def prepare_dataset(voxel_size, source, target):
    # print(":: Load two point clouds and disturb initial pose.")

    #Demo models (room & chair)
    # source = o3d.io.read_point_cloud("cloud_bin_0.pcd")
    # target = o3d.io.read_point_cloud("cloud_bin_1.pcd")

    #Rover Models
    # source = o3d.io.read_point_cloud("ARRVR.pcd")
    # target = o3d.io.read_point_cloud("ARSFVR.pcd")

    #test01
    # source = o3d.io.read_point_cloud("rover_recon_test01.pcd")
    # target = o3d.io.read_point_cloud("rover_predef_test01.pcd")

    #Octagon Models
    # source = o3d.io.read_point_cloud("ReconstructedCenteredOctagon.pcd")
    # source = o3d.io.read_point_cloud("recon-source-phone-02.pcd")

    # source = o3d.io.read_point_cloud("closeup-scene-source-test03-hololens.pcd")
    # target = o3d.io.read_point_cloud("TargetOctagonRealPos01.pcd")

    #displays the models without transformation/rotation
    # draw_registration_result(source, target, np.identity(4))
    # initT = np.matrix('0 0 0 0; 0 0 0 0; 0 0 0 0; 0 0 0 0')
    # draw_registration_result(source, target, initT)

    # vv TESTING INIT TRANSFORM vv #

    # eulerAngleInitTransform = [-126,-4.92,0]
    # initTransformMatrix = Rotation.from_euler('xyz', eulerAngleInitTransform, degrees=True).as_matrix()
    # iTMArray = np.asmatrix(initTransformMatrix)
    # #iTMArray = np.matrix('0 0 0 ; 0 0 0 ; 0 0 0')
    # iTMArray = np.vstack([iTMArray,[0,0,0]])
    # iTMArray = np.hstack([iTMArray,[[0],[0],[0],[1]]])
    # # iTMArray = [[ 9.98223727e-01,  1.53457503e-03, -5.95569937e-02, 0], #-1.24349784e+02],
    # #             [-4.45017673e-02, -6.45436421e-01, -7.62516504e-01, 0], #3.39931651e+01],
    # #             [-3.96103916e-02,  7.63812458e-01, -6.44221659e-01, 0], #5.17655973e+02],
    # #             [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]]
    # draw_registration_result(source, target, iTMArray)
    # source.transform(iTMArray)

    # ^^ TESTING INIT TRANSFORM ^^ #


    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh
    

#RANSAC 
def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    # distance_threshold = voxel_size * 300
    # print(":: RANSAC registration on downsampled point clouds.")
    # print("   Since the downsampling voxel size is %.3f," % voxel_size)
    # print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, False, distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        4, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], 
        # o3d.pipelines.registration.RANSACConvergenceCriteria(4000000, 500))
        o3d.pipelines.registration.RANSACConvergenceCriteria(4000000, 1000000))
    # result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
    #     source_down, target_down, source_fpfh, target_fpfh, distance_threshold)
    return result


# Fast RANSAC
def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.5
    # print(":: Apply fast global registration with distance threshold %.3f" \
    #         % distance_threshold)
    result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    return result


# Local refinement with point-to-plane ICP
def refine_registration(source, target, source_fpfh, target_fpfh, voxel_size, result_ransac):
    distance_threshold = voxel_size * 0.4
    # print(":: Point-to-plane ICP registration is applied on original point")
    # print("   clouds to refine the alignment. This time we use a strict")
    # print("   distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, result_ransac.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    return result

# scaledSourcePCD = o3d.io.read_point_cloud("ScaledRover_90CCW_Cropped.pcd")
# target = o3d.io.read_point_cloud("PreDefRover.pcd")
# source_temp = copy.deepcopy(scaledSourcePCD)
# # eulerAngleInitTransform = [-126,-4.92,0]
# eulerAngleInitTransform = [129.69622076, 25.76793375, 11.84078905]
# initTransformMatrix = Rotation.from_euler('xyz', eulerAngleInitTransform, degrees=True).as_matrix()
# iTMArray = np.asarray(initTransformMatrix)
# iTMArray = np.vstack([iTMArray,[0,0,0]])
# iTMArray = np.hstack([iTMArray,[[0],[0],[0],[0]]])
# # scaledTargetPCD.transform(iTMArray)
# # t = np.matrix('0 0 0 0; 0 0 0 0; 0 0 0 0; 0 0 0 0')
# draw_registration_result(scaledSourcePCD, target, iTMArray)