# print("Hello, friend")

def sendTestData():
    print("made it!")
    # dataVec = [30,90,50]
    # dataVec = [ 0, 90, 0]
    dataVec = [ 0, 45, 0]
    dataStr = "[6,7,8]"

    return dataVec

# import numpy as np
# import copy
# from scipy.spatial.transform import Rotation

# eulerAngleInitTransform = [-126,-4.92,0]
# initTransformMatrix = Rotation.from_euler('xyz', eulerAngleInitTransform, degrees=True).as_matrix()
# iTMArray = np.asarray(initTransformMatrix)
# iTMArray = np.vstack([iTMArray,[0,0,0]])
# iTMArray = np.hstack([iTMArray,[[0],[0],[0],[0]]])
# print(iTMArray)