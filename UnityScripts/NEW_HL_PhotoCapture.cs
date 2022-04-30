using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Windows.Speech;
using UnityEngine.Windows.WebCam;
using Vuforia;

public class NEW_HL_PhotoCapture : MonoBehaviour
{
    PhotoCapture photoCaptureObject = null;
    bool enableVuforia = false;
    private bool takePics = false; //used for stopping and starting the picture taking process
    public int numOfPics; //counts the number of pictures taken

    public List<string> imageFileNames = new List<string>();

    void Start()
    {
        numOfPics = 0;
        VuforiaBehaviour.Instance.enabled = true; //enables Vuforia
    }

    public void startPicProcess()
    {
        takePics = true;
        Debug.Log("Photo Button Pressed");
    }

    void Update()
    {
        if (takePics == true)
        {
            takePics = false;
            VuforiaBehaviour.Instance.enabled = false;
            Debug.Log("Taking a Photo...");
            TakePicture();
        }
    }

    //starts the picture taking process
    void TakePicture()
    {
        numOfPics += 1; //adds 1 every time a pic is taken
        PhotoCapture.CreateAsync(false, OnPhotoCaptureCreated);
    }


    void OnPhotoCaptureCreated(PhotoCapture captureObject)
    {
        //Debug.Log("Made it into OnPhotoCaptureCreated");
        photoCaptureObject = captureObject;
        Resolution cameraResolution = PhotoCapture.SupportedResolutions.OrderByDescending((res) => res.width * res.height).First();
        CameraParameters c = new CameraParameters();
        c.hologramOpacity = 0.0f;
        c.cameraResolutionWidth = cameraResolution.width;
        c.cameraResolutionHeight = cameraResolution.height;
        c.pixelFormat = CapturePixelFormat.BGRA32;
        captureObject.StartPhotoModeAsync(c, OnPhotoModeStarted);
    }
    void OnStoppedPhotoMode(PhotoCapture.PhotoCaptureResult result)
    {
        //Debug.Log("Made it into OnStoppedPhotoMode");
        photoCaptureObject.Dispose();
        photoCaptureObject = null;
    }

    private void OnPhotoModeStarted(PhotoCapture.PhotoCaptureResult result)
    {
        //Debug.Log("Made it into OnPhotoModeStarted");
        if (result.success)
        {
            //Debug.Log("Made it into OnPhotoModeStarted: result SUCCESS");
            string filename = string.Format("Pic" + numOfPics + ".jpg", Time.time);
            imageFileNames.Add(filename);

            //PC path
            //string filePath = System.IO.Path.Combine("C:\\Users\\Braden\\Desktop\\ECEN 404\\FromUnity\\", filename);

            //HoloLens path
            string filePath = System.IO.Path.Combine(Application.persistentDataPath, filename);

            photoCaptureObject.TakePhotoAsync(filePath, PhotoCaptureFileOutputFormat.JPG, OnCapturedPhotoToDisk);
        }
        else
        {
            Debug.LogError("Unable to start photo mode!");
        }
    }
    void OnCapturedPhotoToDisk(PhotoCapture.PhotoCaptureResult result)
    {
        //Debug.Log("Made it into OnCapturedPhotoToDisk");
        if (result.success)
        {
            Debug.Log("Saved Photo to disk!");
            photoCaptureObject.StopPhotoModeAsync(OnStoppedPhotoMode);


            VuforiaBehaviour.Instance.enabled = true;
        }
        else
        {
            Debug.Log("Failed to save Photo to disk");
        }
    }
}
