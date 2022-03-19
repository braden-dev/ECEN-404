from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import cgi
import time
from sqlConnection import *
import os
import subprocess
import sys
from test import *
from ComparisonImplementation import *

hostName = "0.0.0.0"
serverPort = 8000

class MyServer(BaseHTTPRequestHandler):

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
            getImagesFromDB() 

            # Runs the model reconstruction pipeline from the images in the database and outputs it to a folder
            # os.system('python ..\\OpenMVS\\ModelReconstructionPipeline-Thesis.py "C:\\Users\\Braden\\Desktop\\ECEN 404\\FromDatabase" "C:\\Users\\Braden\\Desktop\\ECEN 404\\MvgMvsOutput-Pipeline"')

            # Copies the Dense Mesh file from the reconstruction pipeline output
            # os.system('copy ..\\MvgMvsOutput-Pipeline\\mvs\\scene_dense_mesh_refine.ply') # real file
            os.system('copy ..\\OpenMVS\\reconstruction_testing\\output\\output_set17\\mvs\\scene_dense_mesh_refine.ply') # test file

            # Turns that .ply file into a .pcd (point cloud) file to compare
            os.system('python PCD-FileGeneration.py')

            # Calls the function in the ComparisonImplementation script that compares the two point clouds
            # output = nRANSAC_onceICP()

            # Writes the output (in the form [ x y z]) to the server which send that back to Unity )
            # self.wfile.write(bytes(str(output), "utf-8"))

            # Clears the files from the database preparing it for the next set of images
            clearDatabase()
        
        #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html') 
        self.end_headers()

        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
        formList = form.getlist("imageFromUnity")
        #print("formList length: " + str(len(formList)))
        for i in range(len(formList)):
            value = formList[i]
            insert_images(value, (i+1))

        self.wfile.write("POST request for {}".
                    format(self.path).encode('utf-8'))

#main that runs the server
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
        webServer.server_close()