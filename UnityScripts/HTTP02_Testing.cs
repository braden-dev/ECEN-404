using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using UnityEngine;


public class HTTP02_Testing : MonoBehaviour
{
    string uploadURL = "http://localhost:8888";
    string getURL = "http://localhost:8888/result";

    List<string> imageNames = new List<string>();

    // Start is called before the first frame update
    void Start()
    {
        for(int i = 1; i <= 11; i++)
        {
            imageNames.Add("Pic" + i + ".jpg");
        }
        StartCoroutine(Upload(imageNames));
    }

    // Update is called once per frame
    void Update()
    {

    }

    IEnumerator Upload(List<string> fileNames)
    {
        //creates a new form to post the images into to be sent to the SQL server
        WWWForm postForm = new WWWForm();
        for (int i = 0; i < fileNames.Count; i++)
        {
            //Use the Application.persistentDataPath when on the HoloLens, the other URL is purely for testing locally
            //string filePath = System.IO.Path.Combine(Application.persistentDataPath, fileNames[i]);
            string filePath = System.IO.Path.Combine("C:\\Users\\Braden\\Desktop\\Python Web Server\\FromUnity\\", fileNames[i]);
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
            // Show results as text
            //Debug.Log(www.downloadHandler.text);
            Debug.Log("NO ERRORS, WHOOP WHOOP");
        }
    }

}
