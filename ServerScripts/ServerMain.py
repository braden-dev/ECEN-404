from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import cgi
from sqlConnection import *
from test import *
from PCDFileParser import *
from ComparisonImplementation import *
import os
import open3d as o3d

hostName = "0.0.0.0"
serverPort = 8000

class MyServer(BaseHTTPRequestHandler):

    # GET request for the server
    # Used to send the rotation data back to Unity once all the scripts run
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if(self.path == "/result"):
            # getImagesFromDB()
            #OpenMVG files that will do 3D reconstruciton on the images
            #exec(open("MVG_test01.py").read())

            #test script to be run when testing
            # print(testResult)
            getImagesFromDB()
            testResult = sendTestData()
            self.wfile.write(bytes(str(testResult), "utf-8"))
            clearDatabase()

        #model reconstruction pipeline runs
        if(self.path == "/mrp"):
            # Gets the images from the database
            print("Retrieving Images From the Database...")
            getImagesFromDB() 
            print("Retrieved Images Successfully.")

            # # Runs the model reconstruction pipeline from the images in the database and outputs it to a folder
            # print("Reconstructing the 3D Model...")
            # os.system('python ..\\OpenMVS\\ModelReconstructionPipeline-Thesis.py "C:\\Users\\Braden\\Desktop\\ECEN 404\\FromDatabase" "C:\\Users\\Braden\\Desktop\\ECEN 404\\MvgMvsOutput-Pipeline"')
            # print("Model Reconstruction Complete.")

            # # Copies the Dense Mesh file from the reconstruction pipeline output
            # os.system('copy ..\\MvgMvsOutput-Pipeline\\mvs\\scene_dense_mesh_refine.ply') # real file
            # # os.system('copy ..\\OpenMVS\\reconstruction_testing\\output\\output_set17\\mvs\\scene_dense_mesh_refine.ply') # test file

            # # Turns that .ply file into a .pcd (point cloud) file to compare
            # os.system('python PCDFileGeneration.py')

            # # Uses density maps to crop some unnecessary points - function from PCDFileParser.py
            # runCroppingProcess()

            # # Calls the function in the ComparisonImplementation script that compares two point clouds
            # source = o3d.io.read_point_cloud("CroppedPCDOutputFile.pcd") # standard output file from runCroppingProcess()
            # # this may change depending on the type of object being looked at
            # # can maybe specify this within Unity or something so that the server
            # # knows what point cloud to compare the reconstructed point cloud with
            # #target = o3d.io.read_point_cloud("BEST-reconstruction-edited-realpos01.pcd") 

            # scalePCD("CroppedPCDOutputFile.pcd", 100)
            # #scalePCD("BEST-reconstruction-edited-realpos01.pcd", 100)

            # scaledSourcePCD = o3d.io.read_point_cloud("ScaledCroppedPCDOutputFile.pcd")
            # scaledTargetPCD = o3d.io.read_point_cloud("ScaledBEST-reconstruction-edited-realpos01.pcd")

            ### vv TESTING (DELETE) vv ###
            
            # Targets (pre-defined models)
            #target = o3d.io.read_point_cloud("PreDefRover.pcd")
            target = o3d.io.read_point_cloud("PreDefRover_XZOrient01.pcd")
            #target = o3d.io.read_point_cloud("Octagon_PreDef_XZOrient01.pcd")

            # Ground/Flat models
            # ground = o3d.io.read_point_cloud("GROUND.pcd")
            # ground = o3d.io.read_point_cloud("GROUND-Small.pcd")

            # Rover -- recon. point clouds
            # sourceCloudName = "Rover_InitPos_Cropped.pcd" # ROVER 0
            # sourceCloudName = "Rover_90CW_Cropped.pcd" # ROVER 90 CW (OR 270 CCW)
            # sourceCloudName = "Rover_45CCW_Cropped.pcd" # Rover 45 CCW
            sourceCloudName = "Rover_90CCW_Cropped.pcd" # ROVER 90 CCW

            # Octagon -- recon. point clouds
            # sourceCloudName = "Octagon_0Deg_Recon.pcd" # OCTAGON 0
            # sourceCloudName = "Octagon_90CCW_Recon.pcd" # OCTAGON 90 CCW

            ### ^^ TESTING (DELETE) ^^ ###
            
            # Used to align the recon. model with the horizontal plane
            ground = o3d.io.read_point_cloud("GROUND-Small.pcd")

            # 720 for rover & octagon
            scalePCD(sourceCloudName, 720)
            scaledSourceCloudName = "Scaled" + sourceCloudName

            scaledSourcePCD = o3d.io.read_point_cloud(scaledSourceCloudName)

            # Initial transformation to align the reconstructed model with the horizontal plane (mostly)
            # eulerAngleInitTransform = [-120,0,0]
            eulerAngleInitTransform = [-120,-45,0]
            initTransformMatrix = Rotation.from_euler('xyz', eulerAngleInitTransform, degrees=True).as_matrix()
            firstTransformMatrix = np.asmatrix(initTransformMatrix)
            firstTransformMatrix = np.vstack([firstTransformMatrix,[0,0,0]])
            firstTransformMatrix = np.hstack([firstTransformMatrix,[[0],[0],[0],[1]]])
            #draw_registration_result(scaledSourcePCD, target, iTMArray)
            scaledSourcePCD = scaledSourcePCD.transform(firstTransformMatrix)

            # Arbitrary number to begin the while loop
            firstX = 1000

            # Used to get the X and Y orientations needed to fully
            # align the reconstructed model with the horizontal plane
            while(float(firstX) > 20 or float(firstX) < -20):
                comparisonWithPlane = nRANSAC_onceICP(ground, scaledSourcePCD, 1, False) # First comparison

                newOrient = (str(comparisonWithPlane).split(" "))
                numSpaces = newOrient.count("")
                numBrackets = newOrient.count("[")
                for i in range(numSpaces):
                    newOrient.remove("")
                for j in range(numBrackets):
                    newOrient.remove("[")
                firstX = newOrient[0]
                firstY = newOrient[1]
                if(firstX[0] == '['): 
                    firstX = firstX[1:-1]
                print(newOrient)
                print(f"FirstX: {firstX}")
                print(f"FirstY: {firstY}")

            # Reorients the recon. model with the horizontal plane
            secondTransform = [float(firstX), float(firstY), 0]
            secondTransformMatrix = Rotation.from_euler('xyz', secondTransform, degrees=True).as_matrix()
            secondTransformArray = np.asmatrix(secondTransformMatrix)
            secondTransformArray = np.vstack([secondTransformArray,[0,0,0]])
            secondTransformArray = np.hstack([secondTransformArray,[[0],[0],[0],[1]]])
            scaledSourcePCD = scaledSourcePCD.transform(secondTransformArray)


            print("Comparing the 3D Models...")
            output = nRANSAC_onceICP(target, scaledSourcePCD, 20, True) # Second comparison -- comparing pre-def and recon. models together
            print(f"The 3D Model Comparison Results are: {output}")


            # Writes the output (in the form [ x y z ]) to the server which sends that back to Unity
            print("Sending the Result Back To the Client...")
            self.wfile.write(bytes(str(output), "utf-8"))

            # Clears the files from the database preparing it for the next set of images
            clearDatabase()
        
        #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))

    # POST request to the server
    # Used to allow Unity to send the pictures taken to the server/database
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html') 
        self.end_headers()

        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
        formList = form.getlist("imageFromUnity") # the form contains all the stuff sent from unity, and the list contains all the pictures
        #print("formList length: " + str(len(formList)))
        for i in range(len(formList)):
            value = formList[i]
            insert_images(value, (i+1)) # inserts the images into the database

        self.wfile.write("POST request for {}".
                    format(self.path).encode('utf-8'))

# main that runs the server
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
        webServer.server_close()