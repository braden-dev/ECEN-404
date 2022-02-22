using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using UnityEngine;


public class HTTP_Testing : MonoBehaviour
{
    string uploadURL = "http://localhost:8888";
    string getURL = "http://loclahost:8888/request";

    List<string> imageNames;
    HololensPhotoCapture data;

    // Start is called before the first frame update
    void Start()
    {
        data = GetComponent <HololensPhotoCapture>();
        imageNames = data.imageFileNames;
        StartCoroutine(Upload(imageNames));
        StartCoroutine(GetRequest(getURL));
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    IEnumerator Upload(List<string> fileNames)
    {
        WWWForm postForm = new WWWForm();
        for (int i = 0; i < fileNames.Count; i++)
        {
            string filePath = System.IO.Path.Combine(Application.persistentDataPath, fileNames[i]);
            WWW localFile = new WWW(filePath);
            yield return localFile;
            if (localFile.error == null)
                Debug.Log("Loaded file successfully");
            else
            {
                Debug.Log("Open file error: " + localFile.error);
                yield break; // stop the coroutine here
            }
            postForm.AddBinaryData("theFile", localFile.bytes, fileNames[i], "text/plain");
        }

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
            }
        }
    }

    IEnumerator GetRequest(string uri)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(uri))
        {
            // Request and wait for the desired page.
            yield return webRequest.SendWebRequest();

            string[] pages = uri.Split('/');
            int page = pages.Length - 1;

            switch (webRequest.result)
            {
                case UnityWebRequest.Result.ConnectionError:
                case UnityWebRequest.Result.DataProcessingError:
                    Debug.LogError(pages[page] + ": Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.ProtocolError:
                    Debug.LogError(pages[page] + ": HTTP Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.Success:
                    Debug.Log(pages[page] + ":\nReceived: " + webRequest.downloadHandler.text);
                    break;
            }
        }
    }

}
