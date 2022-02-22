using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using Vuforia;

//This script writes the position and rotation data of the roverModel and the octagonModel to .csv files
public class WritePositionAndRotationData : MonoBehaviour
{
    GameObject roverModel;
    GameObject octagonModel;
    private float period = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        roverModel = GameObject.Find("ModelTargetVikingRover");
        octagonModel = GameObject.Find("ModelTargetOctagon");
    }

    // Update is called once per frame
    void Update()
    {
        if (period >= 1.0f)
        {
            //writes to the rover csv files if the rover is tracked
            if (roverModel.GetComponent<ModelTargetBehaviour>().TargetStatus.Status.Equals(Status.TRACKED))
            {
                WriteToRoverCSVFile();
            }
            //writes to the cylinder csv files if the octagon is tracked
            if (octagonModel.GetComponent<ModelTargetBehaviour>().TargetStatus.Status.Equals(Status.TRACKED))
            {
                WriteToOctagonCSVFile();
            }
            period = 0;
        }
        period += Time.deltaTime;   
    }

    void WriteToRoverCSVFile()
    {
        string fileNamePos = "RoverModelPositionData.csv";
        string fileNameOri = "RoverModelRotationData.csv";

        //HoloLens Paths
        string filePathPos = System.IO.Path.Combine(Application.persistentDataPath, fileNamePos);
        string filePathOri = System.IO.Path.Combine(Application.persistentDataPath, fileNameOri);

        //PC Paths
        //string filePathPos = "C:\\Users\\Braden\\OneDrive\\HoloLensShared\\UnityData\\RoverModelPositionData.csv";
        //string filePathOri = "C:\\Users\\Braden\\OneDrive\\HoloLensShared\\UnityData\\RoverModelRotationData.csv";


        StreamWriter swPos = new StreamWriter(filePathPos, true);
        StreamWriter swOri = new StreamWriter(filePathOri, true);

        swPos.WriteLine(roverModel.GetComponent<ModelTargetBehaviour>().transform.position);
        swOri.WriteLine(roverModel.GetComponent<ModelTargetBehaviour>().transform.eulerAngles);

        swPos.Close();
        swOri.Close();
    }

    void WriteToOctagonCSVFile()
    {
        string fileNamePos = "OctagonModelPositionData.csv";
        string fileNameOri = "OctagonModelRotationData.csv";

        //HoloLens Paths
        string filePathPos = System.IO.Path.Combine(Application.persistentDataPath, fileNamePos);
        string filePathOri = System.IO.Path.Combine(Application.persistentDataPath, fileNameOri);

        //PC Paths
        //string filePathPos = "C:\\Users\\Braden\\OneDrive\\HoloLensShared\\UnityData\\OctagonModelPositionData.csv";
        //string filePathOri = "C:\\Users\\Braden\\OneDrive\\HoloLensShared\\UnityData\\OctagonModelRotationData.csv";

        StreamWriter swPos = new StreamWriter(filePathPos, true);
        StreamWriter swOri = new StreamWriter(filePathOri, true);

        swPos.WriteLine(octagonModel.GetComponent<ModelTargetBehaviour>().transform.position);
        swOri.WriteLine(octagonModel.GetComponent<ModelTargetBehaviour>().transform.eulerAngles);

        swPos.Close();
        swOri.Close();
    }
}
