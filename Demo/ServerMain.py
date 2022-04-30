from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import cgi
from sqlConnection import *
from test import *
from PCDFileParser import *
from ComparisonImplementation import *
import os
import time
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

        if(self.path == "/demo"):
            # Gets the images from the database
            print("Retrieving Images From the Database...")
            getImagesFromDB() 
            print("Retrieved Images Successfully.")

            # Turns that .ply file into a .pcd (point cloud) file to compare
            #os.system('python PCDFileGeneration.py')

            # Uses density maps to crop some unnecessary points - function from PCDFileParser.py
            runCroppingProcess()

            target = o3d.io.read_point_cloud("predefinedBH.pcd")
            sourceCloudName = "Cropped2PCDOutputFile.pcd" # Name might change depending on how much cropping is needed

            # 720 for rover & octagon
            scalePCD(sourceCloudName, 1.1)
            scaledSourceCloudName = "Scaled" + sourceCloudName

            scaledSourcePCD = o3d.io.read_point_cloud(scaledSourceCloudName)

            # print("Comparing the 3D Models...")
            # output = nRANSAC_onceICP(target, scaledSourcePCD, 20, True) # Second comparison -- comparing pre-def and recon. models together
            # print(f"The 3D Model Comparison Results are: {output}")


            # Writes the output (in the form [ x y z ]) to the server which sends that back to Unity
            # print("Sending the Result Back To the Client...")
            # self.wfile.write(bytes(str(output), "utf-8"))

            # Clears the files from the database preparing it for the next set of images
            clearDatabase()


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