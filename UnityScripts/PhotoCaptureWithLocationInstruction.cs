using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using UnityEngine.Windows.Speech;
using UnityEngine.Windows.WebCam;
using Vuforia;

public class PhotoCaptureWithLocationInstruction : MonoBehaviour
{

    PhotoCapture photoCaptureObject = null;
    private bool takePics = false; //used for stopping and starting the picture taking process
    private KeywordRecognizer keywordRecognizerStart;
    private float period = 0.0f;
    private int startOnce;
    GameObject MainCamera;
    GameObject Rover;
    GameObject PCM;

    // Start is called before the first frame update
    void Start()
    {
        VuforiaBehaviour.Instance.enabled = true;
        List<string> keywordStart = new List<string>();
        keywordStart.Add("Start");
        keywordRecognizerStart = new KeywordRecognizer(keywordStart.ToArray());
        keywordRecognizerStart.Start();
        MainCamera = GameObject.Find("Main Camera");
        Rover = GameObject.Find("ModelTargetVikingRover");
        PCM = GameObject.Find("PhotoCaptureMarker");
    }

    // Update is called once per frame
    void Update()
    {
        startOnce = 1;
        keywordRecognizerStart.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognizedStart;

        if(takePics == true)
        {
            takePics = false;
            Debug.Log("Saving a photo.");
            TakePicture();
        }

        PCM.transform.position = new Vector3(Rover.transform.position.x - 0.2f, Rover.transform.position.y, Rover.transform.position.x - 0.2f);

        if (period >= 3.0f)
        {
            InRightLocation();
            period = 0;
        }
        period += Time.deltaTime;
        

    }

    private void KeywordRecognizer_OnPhraseRecognizedStart(PhraseRecognizedEventArgs args)
    {
        while (startOnce == 1)
        {
            Debug.Log("Start recognized.");
            takePics = true;
            VuforiaBehaviour.Instance.enabled = false;

            startOnce = 2;
        }
    }

    private void InRightLocation()
    {
        if(MainCamera.transform.position.x - PCM.transform.position.x >= -0.05 || MainCamera.transform.position.x - PCM.transform.position.x <= 0.05)
        {
            if (MainCamera.transform.position.z - PCM.transform.position.z >= -0.05 || MainCamera.transform.position.z - PCM.transform.position.z <= 0.05)
            {
                takePics = true;
            }
        }
    }

    void TakePicture()
    {
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
        VuforiaBehaviour.Instance.enabled = true;
    }

    private void OnPhotoModeStarted(PhotoCapture.PhotoCaptureResult result)
    {
        //Debug.Log("Made it into OnPhotoModeStarted");
        if (result.success)
        {
            //Debug.Log("Made it into OnPhotoModeStarted: result SUCCESS");
            string filename = string.Format(@"CapturedImage{0}_n.jpg", Time.time);

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
