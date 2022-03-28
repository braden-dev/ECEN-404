from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import cgi
from sqlConnection import *
from test import *
from PCDFileParser import *
from ComparisonImplementation import *
import os
import open3d as o3d

# import subprocess
# import sys
# import time

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
            # # Gets the images from the database
            # print("Retrieving Images From the Database...")
            # getImagesFromDB() 
            # print("Retrieved Images Successfully.")

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
            # target = o3d.io.read_point_cloud("BEST-reconstruction-edited-realpos01.pcd") 

            # scalePCD("CroppedPCDOutputFile.pcd", 100)
            # scalePCD("BEST-reconstruction-edited-realpos01.pcd", 100)

            # scaledSourcePCD = o3d.io.read_point_cloud("ScaledCroppedPCDOutputFile.pcd")
            # scaledTargetPCD = o3d.io.read_point_cloud("ScaledBEST-reconstruction-edited-realpos01.pcd")

            # DELETE vv
            # Calls the function in the ComparisonImplementation script that compares two point clouds
            source = o3d.io.read_point_cloud("s.pcd") # standard output file from runCroppingProcess()
            # this may change depending on the type of object being looked at
            # can maybe specify this within Unity or something so that the server
            # knows what point cloud to compare the reconstructed point cloud with
            target = o3d.io.read_point_cloud("t.pcd") 

            # scalePCD("s.pcd", 100)
            # scalePCD("t.pcd", 100)

            scaledSourcePCD = o3d.io.read_point_cloud("s.pcd")
            scaledTargetPCD = o3d.io.read_point_cloud("t.pcd")
            # DELETE ^^

            print("Comparing the 3D Models...")
            output = nRANSAC_onceICP(scaledSourcePCD, scaledTargetPCD)
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