using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Windows.Speech;
using UnityEngine.Windows.WebCam;
using Vuforia;

public class HololensPhotoCapture : MonoBehaviour
{
    PhotoCapture photoCaptureObject = null;
    private bool goAgain = true;
    private float period = 0.0f;
    private bool takePics = false; //used for stopping and starting the picture taking process
    private KeywordRecognizer keywordRecognizerStart;
    private KeywordRecognizer keywordRecognizerStop;

    public List<string> imageFileNames = new List<string>();

    private int startOnce, stopOnce;
    //testing adding keywords for the hololens

    void Start()
    {
        VuforiaBehaviour.Instance.enabled = true;
        //Subscribing events to when Vuforia is paused or unpaused
        VuforiaApplication.Instance.OnVuforiaPaused += OnVuforiaPaused;
        // Setup a keyword recognizer.
        List<string> keywordStart = new List<string>();
        List<string> keywordStop = new List<string>();
        keywordStart.Add("Start");
        keywordStop.Add("Stop");
        keywordRecognizerStart = new KeywordRecognizer(keywordStart.ToArray());
        keywordRecognizerStop = new KeywordRecognizer(keywordStop.ToArray());
        keywordRecognizerStart.Start();
        keywordRecognizerStop.Start();
    }

    // Handle the keyword "Start" to start taking pictures.
    private void KeywordRecognizer_OnPhraseRecognizedStart(PhraseRecognizedEventArgs args)
    {
        while (startOnce == 1)
        {
            Debug.Log("Start recognized.");
            VuforiaBehaviour.Instance.enabled = false;

            startOnce = 2;
        }
    }

    // Handle the keyword "Stop" to stop taking pictures.
    private void KeywordRecognizer_OnPhraseRecognizedStop(PhraseRecognizedEventArgs args)
    { 
        while (stopOnce == 1)
        {
            Debug.Log("Stop recognized.");

            VuforiaBehaviour.Instance.enabled = true;

            stopOnce = 2;
        }
    }

    //starts the picture taking process
    void TakePicture()
    {
        goAgain = false;
        PhotoCapture.CreateAsync(false, OnPhotoCaptureCreated);
    }

    //this runs when Vuforia pauses and it allows for pictures to be taken
    void OnVuforiaPaused(bool paused)
    {
        if (paused)
        {
            takePics = true;
        }
        if (!paused)
        {
            takePics = false;
        }
    }

    void Update()
    {
        startOnce = 1;
        stopOnce = 1;
        keywordRecognizerStart.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognizedStart;
        keywordRecognizerStop.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognizedStop;

        if (takePics == true)
        {
            if (period >= 3.0f)
            {
                if (goAgain == true)
                {
                    Debug.Log("Saving another photo.");
                    TakePicture();
                }
                period = 0;
            }
            period += Time.deltaTime;
        }
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
        goAgain = true;
    }

    private void OnPhotoModeStarted(PhotoCapture.PhotoCaptureResult result)
    {
        //Debug.Log("Made it into OnPhotoModeStarted");
        if (result.success)
        {
            //Debug.Log("Made it into OnPhotoModeStarted: result SUCCESS");
            string filename = string.Format(@"CapturedImage{0}_n.jpg", Time.time);
            imageFileNames.Add(filename);

            //PC path
            //string filePath = System.IO.Path.Combine("C:\\Users\\Braden\\OneDrive\\HoloLensShared\\UnityPics\\", filename);

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
        }
        else
        {
            Debug.Log("Failed to save Photo to disk");
        }
    }
}
