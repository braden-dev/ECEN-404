from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import cgi
import time
from sqlConnection import *
import os
import subprocess
import sys
from test import *

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

        if(self.path == "/mrp"):
            os.system('python ..\\OpenMVS\\ModelReconstructionPipeline-Thesis.py "C:\\Users\\Braden\\Desktop\\ECEN 404\\FromDatabase" "C:\\Users\\Braden\\Desktop\\ECEN 404\\MvgMvsOutput"')
        
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