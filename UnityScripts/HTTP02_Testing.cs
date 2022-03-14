using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using UnityEngine;
using UnityEngine.Windows.Speech;


public class HTTP02_Testing : MonoBehaviour
{
    string uploadURL = "http://192.168.0.25:8000";
    string getURL = "http://192.168.0.25:8000/result";

    private int numPics;

    private int sendOnce;
    private KeywordRecognizer keywordRecognizerSend;

    List<string> imageNames = new List<string>();

    // Start is called before the first frame update
    void Start()
    {
        numPics = 0;

        List<string> keywordSend = new List<string>();
        keywordSend.Add("Send");
        keywordRecognizerSend = new KeywordRecognizer(keywordSend.ToArray());
        keywordRecognizerSend.Start();

        //StartCoroutine(GetRequest(getURL));  

        //Debug.Log("App persistent data path: " + Application.persistentDataPath);
    }

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
            gameObject.GetComponent<HololensPhotoCapture>().numOfPics = 0;
        }
    }

    // Update is called once per frame
    void Update()
    {
        numPics = gameObject.GetComponent<HololensPhotoCapture>().numOfPics;
        sendOnce = 1;
        keywordRecognizerSend.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognizedSend;
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

    IEnumerator Upload(List<string> fileNames)
    {
        //creates a new form to post the images into to be sent to the SQL server
        WWWForm postForm = new WWWForm();
        for (int i = 0; i < fileNames.Count; i++)
        {
            //Use the Application.persistentDataPath when on the HoloLens, the other URL is purely for testing locally
            string filePath = System.IO.Path.Combine(Application.persistentDataPath, fileNames[i]);

            //PC path
            //string filePath = System.IO.Path.Combine("C:\\Users\\Braden\\Desktop\\ECEN 404\\FromUnity\\", fileNames[i]);
            Debug.Log("File path: " + filePath);
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
            Debug.Log("WWW: " + www.downloadHandler.text);
        }
    }

}
