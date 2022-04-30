using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.Windows.Speech;
using Vuforia;


public class ServerDatabaseInteractions : MonoBehaviour
{
    public string uploadURL = "http://192.168.0.10:8000";
    public string getURL = "http://192.168.0.10:8000/result"; //for testing
    // public string getURL = "http ://192.168.0.10:8000/mrp"; //real (remove space after "http")

    private int numPics;

    private int sendOnce;
    private KeywordRecognizer keywordRecognizerSend;

    List<string> imageNames = new List<string>();

    public string outputOrientation = "something is wrong";
    public bool dataReceived;

    GameObject mainCam, photoButton, sendButton, nextButton, checkButton, BHIdentifyCanvas, IdentifyPeg, bh, bhPerch;
    bool run;

    public Vector3 sendButtonPos;

    // Start is called before the first frame update
    void Start()
    {
        mainCam = GameObject.Find("Main Camera");
        bh = GameObject.Find("ModelTargetBirdHouse");
        bhPerch = GameObject.Find("ModelTargetBirdHousePerch");
        photoButton = GameObject.Find("PictureButton");
        sendButton = GameObject.Find("SendButton");
        nextButton = GameObject.Find("NextButton");
        checkButton = GameObject.Find("CheckButton");
        BHIdentifyCanvas = GameObject.Find("BHIdentifyCanvas");
        IdentifyPeg = GameObject.Find("IdentifyPeg");

        sendButtonPos = sendButton.transform.position;

        // Will turn this "true" when the orientation data is received
        dataReceived = false;

        //Debug.Log(Application.persistentDataPath);
        //numPics = 0;
        numPics = gameObject.GetComponent<NEW_HL_PhotoCapture>().numOfPics;

        List<string> keywordSend = new List<string>();
        keywordSend.Add("Send");
        keywordRecognizerSend = new KeywordRecognizer(keywordSend.ToArray());
        keywordRecognizerSend.Start();

        run = true;
    }

    // Runs this function when "Send" is detected
    private void KeywordRecognizer_OnPhraseRecognizedSend(PhraseRecognizedEventArgs args)
    {
        while (sendOnce == 1)
        {
            Debug.Log("Send Detected.");
            Debug.Log("Num of Pics: " + numPics);
            for (int i = 1; i <= numPics; i++)
            {
                imageNames.Add("Pic" + i + ".jpg");
            }
            StartCoroutine(Upload(imageNames));
            sendOnce = 2;
            gameObject.GetComponent<NEW_HL_PhotoCapture>().numOfPics = 0;
            numPics = 0;
        }
    }

    // Update is called once per frame
    void Update()
    {
        numPics = gameObject.GetComponent<NEW_HL_PhotoCapture>().numOfPics;
        sendOnce = 1;
        //keywordRecognizerSend.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognizedSend;

        //if ((SceneManager.GetActiveScene().name == "second-step") && run == true)
        //{
        //    //bh.GetComponent<ModelTargetBehaviour>().enabled = true;
        //    //bhPerch.GetComponent<ModelTargetBehaviour>().enabled = false;
        //    startUpload();
        //    run = false;
        //}

        if (bhPerch.GetComponent<ModelTargetBehaviour>().TargetStatus.Status.Equals(Status.TRACKED))
        {
            nextButton.transform.position = sendButtonPos;
        }

    }

    public void SendButtonPressed()
    {
        //photoButton.transform.position = new Vector3(1000, 1000, 1000);
        photoButton.transform.position = photoButton.transform.position;
        sendButtonPos = sendButton.transform.position;
        sendButton.transform.position = new Vector3(1000, 1000, 1000);
  
        BHIdentifyCanvas.GetComponent<MeshRenderer>().enabled = true;
        checkButton.transform.position = sendButtonPos;

        //startUpload();
    }

    public void CheckButtonPressed()
    {
        //Moves the buttons around and enables/disables
        //some Unity game objects
        BHIdentifyCanvas.GetComponent<MeshRenderer>().enabled = false;
        sendButton.transform.position = checkButton.transform.position;
        photoButton.transform.position = photoButton.transform.position;
        checkButton.transform.position = new Vector3(1000, 1000, 1000);

        //starts the image upload
        startUpload();
        //allows the object of interest to be tracked by Vuforia
        bh.GetComponent<ModelTargetBehaviour>().enabled = true;
    }

    public void startUpload()
    {

        Debug.Log("Send Button Pressed.");
        Debug.Log("Num of Pics: " + numPics);
        //adds all the images taken to a list
        for (int i = 1; i <= numPics; i++)
        {
            imageNames.Add("Pic" + i + ".jpg");
        }
        //uploads the image file to the server
        StartCoroutine(Upload(imageNames));
        //resets the number of pictures
        gameObject.GetComponent<NEW_HL_PhotoCapture>().numOfPics = 0;
        numPics = 0;
    }

    void DeleteFiles(string path)
    {
        foreach (string sFile in System.IO.Directory.GetFiles(path, "*.jpg"))
        {
            System.IO.File.Delete(sFile);
        }

        //clears the array with the names of the images
        imageNames.Clear();
    }

    public IEnumerator Upload(List<string> fileNames)
    {
        //creates a new form to post the images into to be sent to the SQL server
        WWWForm postForm = new WWWForm();
        for (int i = 0; i < fileNames.Count; i++)
        {
            //Use the Application.persistentDataPath when on the HoloLens, the other URL is purely for testing locally
            string filePath = System.IO.Path.Combine(Application.persistentDataPath, fileNames[i]);

            //PC path
            //string filePath = System.IO.Path.Combine("C:\\Users\\Braden\\Desktop\\ECEN 404\\FromUnity\\", fileNames[i]);
            //Debug.Log("File path: " + filePath);
            WWW localFile = new WWW(filePath);
            yield return localFile;
            if (localFile.error == null)
                Debug.Log("Loaded file successfully");
            else
            {
                Debug.Log("Open file error: " + localFile.error);
                yield break; // stop the coroutine here
            }
            postForm.AddBinaryData("imageFromUnity", localFile.bytes, fileNames[i], "text/plain");
        }

        //sends the form to the uploadURL
        using (UnityWebRequest www = UnityWebRequest.Post(uploadURL, postForm))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log("Form upload complete!");
                Debug.Log("Get URL: " + getURL);
                StartCoroutine(GetRequest(getURL));
            }
        }


        DeleteFiles(Application.persistentDataPath);
    }

    //function to request data from the server -- will be used to ask for the processed image/3D model data
    IEnumerator GetRequest(string uri)
    {
        UnityWebRequest www = UnityWebRequest.Get(uri);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            //Show results as text
            //Should get a string or vector/array back with the degree rotations
            //Something like [{x degrees}, {y degress}, {z degrees}]
            outputOrientation = www.downloadHandler.text;
            dataReceived = true;
            Debug.Log("WWW: " + www.downloadHandler.text);
            //mainCam.GetComponent<ServerDatabaseInteractions>().dataReceived = true;
            mainCam.GetComponent<ServerDatabaseInteractions>().dataReceived = true;
            //SceneManager.LoadScene("second-step");
        }
    }

}
