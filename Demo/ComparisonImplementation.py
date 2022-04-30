from ModelComparisonCoreFunctions import *

def nRANSAC_onceICP(sourcePCD, targetPCD, n, showDisplay):
    RANSACcorrespondanceSetSizeVec = []
    ICPcorrespondanceSetSizeVec = []
    # maxRCSS = 0
    maxICPCSS = 0
    # num = 0
    # start = time.time()

    totalRuns = 0
    goodRuns = 0

    # Runs n times 
    for i in range(n):
    # for i in range(10): # <=== CHANGE BACK TO i=10 OR SOMETHING
        #step 1 - pre-processing
        source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(voxel_size, sourcePCD, targetPCD)

        #step 2 - RANSAC
        result_ransac = execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)

        #step 2-b - Fast RANSAC -- INACCURATE
        # result_ransac = execute_fast_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)

        result_ransac_split = str(result_ransac).split(" ")
        RANSACcorrespondanceSetSize = (result_ransac_split[len(result_ransac_split)-5]).split("\n")[0]
        RANSACcorrespondanceSetSizeVec.append(RANSACcorrespondanceSetSize)

        # #step 3 - ICP
        resultICP = refine_registration(source, target, source_fpfh, target_fpfh, voxel_size, result_ransac)
        
        result_icp_split = str(resultICP).split(" ")
        ICPcorrespondanceSetSize = (result_icp_split[len(result_icp_split)-5]).split("\n")[0]

        # ICPcorrespondanceSetSizeVec.append(ICPcorrespondanceSetSize)

        totalRuns += 1

        if(int(ICPcorrespondanceSetSize) >= maxICPCSS * 0.995):
                ICPcorrespondanceSetSizeVec.append(ICPcorrespondanceSetSize)
                if(int(ICPcorrespondanceSetSize) > maxICPCSS):
                    maxICPCSS = int(ICPcorrespondanceSetSize)
                bestICP = resultICP
                goodRuns+=1

    # print(float(goodRuns/totalRuns))
    # print("Total time was %.3f sec." % (time.time() - start))
    # print(RANSACcorrespondanceSetSizeVec)
    # print(ICPcorrespondanceSetSizeVec)
    # print(num)
    if(showDisplay == True):
        draw_registration_result(source, target, bestICP.transformation)

    # count = 0
    # for i in ICPcorrespondanceSetSizeVec:
    #     # print(f"i: {i}")
    #     if(i == '20521'):
    #         count += 1
    # print(f"Count: {count}")
    # print(f"Ratio: {float(count/totalRuns)}")
    # print(bestICP.transformation)

    T = bestICP.transformation.copy() # the 4x4 matrix obtained
    print(T)
    rotation = T[:3, :3] # rotation of the point cloud as a 3x3 matrix
    # translation = T[:3, 3] # translation of the point cloud as a 3x1 matrix

    # set degrees to False if you want radian value
    euler_angle = Rotation.from_matrix(rotation).as_euler('xyz', degrees=True)

    # print("Rotation 3x3 Matrix:")
    # print(rotation)
    # print()
    # print("Rotation in Euler Angles:")
    # print(euler_angle)
    
    return euler_angle