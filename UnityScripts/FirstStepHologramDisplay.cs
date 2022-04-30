using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Vuforia;

public class FirstStepHologramDisplay : MonoBehaviour
{

    GameObject objectOfInterest, poi, objectCenter, mainCam;
    //GameObject objectOfInterest, birdHouse, objectCenter;
    Vector3 objPos, objPoIPos, objCenterPos;
    public Vector3 objPoIOffsetStep1, objPoIOffsetStep2;
    public bool dataReceivedHD;

    public Vector3 newOffset;
    public bool newOffsetCalculated;
    public List<float> orientData;

    //Test
    bool runProcess, updatePos;

    bool run;

    // Start is called before the first frame update
    void Start()
    {
        newOffsetCalculated = false;
        //objectOfInterest = GameObject.Find("ModelTargetVikingRover");
        mainCam = GameObject.Find("Main Camera");
        //arrow = GameObject.Find("simple_arrow_rover");
        //poi = GameObject.Find("VuforiaPosition");
        //objectCenter = GameObject.Find("VuforiaPositionCenter");

        objectOfInterest = GameObject.Find("ModelTargetBirdHouse");
        objectCenter = GameObject.Find("BirdHouseCenter"); //Center of the birdhouse
        poi = GameObject.Find("bhPerchDesiredPos"); // Whatever the object of interest is

        // Bird House
        //objPoIOffsetStep1 = new Vector3(-0.0176f, 0.0571f, -0.0834f);
        objPoIOffsetStep1 = new Vector3(-0.01895f, 0.0575f, -0.0755f);


        //Test
        //runProcess = true;
        runProcess = false;
        updatePos = false;

        run = true;

        orientData = new List<float>();
    }

    // Update is called once per frame
    void Update()
    {
        objPos = objectOfInterest.GetComponent<ModelTargetBehaviour>().transform.position;
        objCenterPos = objectCenter.transform.position;

        //poi.transform.position = objCenterPos + objPoIOffset;

        //if((SceneManager.GetActiveScene().name == "second-step") && run == true)
        //{
        //run = false;
        //dataReceivedHD = true;
        //}


        dataReceivedHD = mainCam.GetComponent<ServerDatabaseInteractions>().dataReceived;
        if (dataReceivedHD == true)
        {
            //Debug.Log("THE DATA HAS BEEN RECEIVED");
            dataReceivedHD = false;

            mainCam.GetComponent<ServerDatabaseInteractions>().dataReceived = false;
            Debug.Log(mainCam.GetComponent<ServerDatabaseInteractions>().outputOrientation);
            orientData = ParseOrientationData(mainCam.GetComponent<ServerDatabaseInteractions>().outputOrientation);
            mainCam.GetComponent<FirstStep>().rotChange = orientData;
            Debug.Log("ORIENT DATA: " + orientData[0] + ", " + orientData[1] + ", " + orientData[2]);
            newOffset = CalculateNewPositions(orientData, objPoIOffsetStep1);
            mainCam.GetComponent<FirstStep>().newOffsetFromHD = newOffset;
            Debug.Log("newOffset = " + newOffset);
        }
    }

    Vector3 CalculateNewPositions(List<float> initOrientations, Vector3 objPoIOffset)
    {
        Vector3 newPos = new Vector3();

        //objPos is xc, yc, and zc

        //objPos = objectOfInterest.GetComponent<ModelTargetBehaviour>().transform.position;
        objPoIPos = objCenterPos + objPoIOffset; //provides x0, y0, z0
        //poi.transform.position = objPoIPos;

        // I think the holo offset is from the PoI but need to double check
        // also this provides x0, y0, and z0
        //hologramPos = objPos + hologramOffset;
        //arrow.transform.position = hologramPos;

        // XZ Orient and XY Orient are swapped between 3D builder and Unity
        float yzOrient = initOrientations[0];
        float xzOrient = initOrientations[2]; //about the z-axis is the y rotation in unity
        float xyOrient = initOrientations[1]; //about the y-axis is the z rotation in unity

        // Implement functions from Python calculate the new postions in each plane
        // Should be simple -- hopefully
        float xc, yc, zc; //Location of the point of interest (center of circle)

        // Commented out for testing
        //objCenterPos = objectCenter.transform.position;
        xc = objCenterPos[0];
        yc = objCenterPos[1];
        zc = objCenterPos[2];

        float x0, y0, z0, x1, y1, z1, theta1, r1;
        x0 = objPoIPos[0];
        y0 = objPoIPos[1];
        z0 = objPoIPos[2];

        Debug.Log($"X0: {x0}, Y0: {y0}, Z0: {z0}");

        // X-Z Plane
        theta1 = (xzOrient * Mathf.PI) / 180;

        r1 = Mathf.Sqrt(Mathf.Pow((xc - x0), 2) + Mathf.Pow((zc - z0), 2));

        x1 = (Mathf.Pow(r1, 2) * Mathf.Cos(theta1) - Mathf.Pow(r1, 2) + Mathf.Pow(x0, 2) - x0 * xc + Mathf.Pow(z0, 2) - z0 * zc + (-z0 + zc) * (-r1 * Mathf.Sqrt(-(Mathf.Cos(theta1) - 1) * (Mathf.Pow(r1, 2) * Mathf.Cos(theta1) - Mathf.Pow(r1, 2) + 2 * Mathf.Pow(x0, 2) - 4 * x0 * xc + 2 * Mathf.Pow(xc, 2) + 2 * Mathf.Pow(z0, 2) - 4 * z0 * zc + 2 * Mathf.Pow(zc, 2))) * (x0 - xc) / (Mathf.Pow(x0, 2) - 2 * x0 * xc + Mathf.Pow(xc, 2) + Mathf.Pow(z0, 2) - 2 * z0 * zc + Mathf.Pow(zc, 2)) + (Mathf.Pow(r1, 2) * z0 * Mathf.Cos(theta1) - Mathf.Pow(r1, 2) * z0 - Mathf.Pow(r1, 2) * zc * Mathf.Cos(theta1) + Mathf.Pow(r1, 2) * zc + Mathf.Pow(x0, 2) * z0 - 2 * x0 * xc * z0 + Mathf.Pow(xc, 2) * z0 + Mathf.Pow(z0, 3) - 2 * Mathf.Pow(z0, 2) * zc + z0 * Mathf.Pow(zc, 2)) / (Mathf.Pow(x0, 2) - 2 * x0 * xc + Mathf.Pow(xc, 2) + Mathf.Pow(z0, 2) - 2 * z0 * zc + Mathf.Pow(zc, 2)))) / (x0 - xc);
        y1 = y0;
        z1 = -r1 * Mathf.Sqrt(-(Mathf.Cos(theta1) - 1) * (Mathf.Pow(r1, 2) * Mathf.Cos(theta1) - Mathf.Pow(r1, 2) + 2 * Mathf.Pow(x0, 2) - 4 * x0 * xc + 2 * Mathf.Pow(xc, 2) + 2 * Mathf.Pow(z0, 2) - 4 * z0 * zc + 2 * Mathf.Pow(zc, 2))) * (x0 - xc) / (Mathf.Pow(x0, 2) - 2 * x0 * xc + Mathf.Pow(xc, 2) + Mathf.Pow(z0, 2) - 2 * z0 * zc + Mathf.Pow(zc, 2)) + (Mathf.Pow(r1, 2) * z0 * Mathf.Cos(theta1) - Mathf.Pow(r1, 2) * z0 - Mathf.Pow(r1, 2) * zc * Mathf.Cos(theta1) + Mathf.Pow(r1, 2) * zc + Mathf.Pow(x0, 2) * z0 - 2 * x0 * xc * z0 + Mathf.Pow(xc, 2) * z0 + Mathf.Pow(z0, 3) - 2 * Mathf.Pow(z0, 2) * zc + z0 * Mathf.Pow(zc, 2)) / (Mathf.Pow(x0, 2) - 2 * x0 * xc + Mathf.Pow(xc, 2) + Mathf.Pow(z0, 2) - 2 * z0 * zc + Mathf.Pow(zc, 2));

        if ((xzOrient > 180 && xzOrient <= 360) || (xzOrient < 0 && xzOrient >= -180))
        {
            //float diff = zc - z1;
            //Debug.Log("Diff = " + diff);
            //Debug.Log("z1 BEFORE = " + z1);
            //z1 = zc +  diff;
            //Debug.Log("z1 AFTER = " + z1);

            float diff = xc - x1;
            //Debug.Log("Diff = " + diff);
            //Debug.Log("z1 BEFORE = " + x1);
            x1 = xc + diff;
            //Debug.Log("z1 AFTER = " + x1);

        }

        Debug.Log($"R1: {r1}, Theta1: {theta1}, X1: {x1}, Y1: {y1}, Z1: {z1}");

        float x2, y2, z2, theta2, r2;
        // X-Y Plane
        theta2 = (xyOrient * Mathf.PI) / 180;
        r2 = Mathf.Sqrt(Mathf.Pow((xc - x1), 2) + Mathf.Pow((yc - y1), 2));

        x2 = (Mathf.Pow(r2, 2) * Mathf.Cos(theta2) - Mathf.Pow(r2, 2) + Mathf.Pow(x1, 2) - x1 * xc + Mathf.Pow(y1, 2) - y1 * yc + (-y1 + yc) * (-r2 * Mathf.Sqrt(-(Mathf.Cos(theta2) - 1) * (Mathf.Pow(r2, 2) * Mathf.Cos(theta2) - Mathf.Pow(r2, 2) + 2 * Mathf.Pow(x1, 2) - 4 * x1 * xc + 2 * Mathf.Pow(xc, 2) + 2 * Mathf.Pow(y1, 2) - 4 * y1 * yc + 2 * Mathf.Pow(yc, 2))) * (x1 - xc) / (Mathf.Pow(x1, 2) - 2 * x1 * xc + Mathf.Pow(xc, 2) + Mathf.Pow(y1, 2) - 2 * y1 * yc + Mathf.Pow(yc, 2)) + (Mathf.Pow(r2, 2) * y1 * Mathf.Cos(theta2) - Mathf.Pow(r2, 2) * y1 - Mathf.Pow(r2, 2) * yc * Mathf.Cos(theta2) + Mathf.Pow(r2, 2) * yc + Mathf.Pow(x1, 2) * y1 - 2 * x1 * xc * y1 + Mathf.Pow(xc, 2) * y1 + Mathf.Pow(y1, 3) - 2 * Mathf.Pow(y1, 2) * yc + y1 * Mathf.Pow(yc, 2)) / (Mathf.Pow(x1, 2) - 2 * x1 * xc + Mathf.Pow(xc, 2) + Mathf.Pow(y1, 2) - 2 * y1 * yc + Mathf.Pow(yc, 2)))) / (x1 - xc);
        y2 = -r2 * Mathf.Sqrt(-(Mathf.Cos(theta2) - 1) * (Mathf.Pow(r2, 2) * Mathf.Cos(theta2) - Mathf.Pow(r2, 2) + 2 * Mathf.Pow(x1, 2) - 4 * x1 * xc + 2 * Mathf.Pow(xc, 2) + 2 * Mathf.Pow(y1, 2) - 4 * y1 * yc + 2 * Mathf.Pow(yc, 2))) * (x1 - xc) / (Mathf.Pow(x1, 2) - 2 * x1 * xc + Mathf.Pow(xc, 2) + Mathf.Pow(y1, 2) - 2 * y1 * yc + Mathf.Pow(yc, 2)) + (Mathf.Pow(r2, 2) * y1 * Mathf.Cos(theta2) - Mathf.Pow(r2, 2) * y1 - Mathf.Pow(r2, 2) * yc * Mathf.Cos(theta2) + Mathf.Pow(r2, 2) * yc + Mathf.Pow(x1, 2) * y1 - 2 * x1 * xc * y1 + Mathf.Pow(xc, 2) * y1 + Mathf.Pow(y1, 3) - 2 * Mathf.Pow(y1, 2) * yc + y1 * Mathf.Pow(yc, 2)) / (Mathf.Pow(x1, 2) - 2 * x1 * xc + Mathf.Pow(xc, 2) + Mathf.Pow(y1, 2) - 2 * y1 * yc + Mathf.Pow(yc, 2));
        z2 = z1;

        //if (xyOrient <= 360 /*180*/ && xyOrient > 180)
        if ((xyOrient > 180 && xyOrient <= 360) || (xyOrient < 0 && xyOrient >= -180))
        {
            //float diff = yc - y2;
            //y2 = yc + diff;

            float diff = xc - x2;
            x2 = xc + diff;
        }

        Debug.Log($"R2: {r2}, Theta2: {theta2}, X2: {x2}, Y2: {y2}, Z2: {z2}");

        float x3, y3, z3, theta3, r3;
        // Y-Z Plane
        theta3 = (yzOrient * Mathf.PI) / 180;
        r3 = Mathf.Sqrt(Mathf.Pow((yc - y2), 2) + Mathf.Pow((zc - z2), 2));

        x3 = x2;
        y3 = (Mathf.Pow(r3, 2) * Mathf.Cos(theta3) - Mathf.Pow(r3, 2) + Mathf.Pow(y2, 2) - y2 * zc + Mathf.Pow(z2, 2) - z2 * zc + (-z2 + zc) * (-r3 * Mathf.Sqrt(-(Mathf.Cos(theta3) - 1) * (Mathf.Pow(r3, 2) * Mathf.Cos(theta3) - Mathf.Pow(r3, 2) + 2 * Mathf.Pow(y2, 2) - 4 * y2 * zc + 2 * Mathf.Pow(zc, 2) + 2 * Mathf.Pow(z2, 2) - 4 * z2 * zc + 2 * Mathf.Pow(zc, 2))) * (y2 - zc) / (Mathf.Pow(y2, 2) - 2 * y2 * zc + Mathf.Pow(zc, 2) + Mathf.Pow(z2, 2) - 2 * z2 * zc + Mathf.Pow(zc, 2)) + (Mathf.Pow(r3, 2) * z2 * Mathf.Cos(theta3) - Mathf.Pow(r3, 2) * z2 - Mathf.Pow(r3, 2) * zc * Mathf.Cos(theta3) + Mathf.Pow(r3, 2) * zc + Mathf.Pow(y2, 2) * z2 - 2 * y2 * zc * z2 + Mathf.Pow(zc, 2) * z2 + Mathf.Pow(z2, 3) - 2 * Mathf.Pow(z2, 2) * zc + z2 * Mathf.Pow(zc, 2)) / (Mathf.Pow(y2, 2) - 2 * y2 * zc + Mathf.Pow(zc, 2) + Mathf.Pow(z2, 2) - 2 * z2 * zc + Mathf.Pow(zc, 2)))) / (y2 - zc);
        z3 = -r3 * Mathf.Sqrt(-(Mathf.Cos(theta3) - 1) * (Mathf.Pow(r3, 2) * Mathf.Cos(theta3) - Mathf.Pow(r3, 2) + 2 * Mathf.Pow(y2, 2) - 4 * y2 * zc + 2 * Mathf.Pow(zc, 2) + 2 * Mathf.Pow(z2, 2) - 4 * z2 * zc + 2 * Mathf.Pow(zc, 2))) * (y2 - zc) / (Mathf.Pow(y2, 2) - 2 * y2 * zc + Mathf.Pow(zc, 2) + Mathf.Pow(z2, 2) - 2 * z2 * zc + Mathf.Pow(zc, 2)) + (Mathf.Pow(r3, 2) * z2 * Mathf.Cos(theta3) - Mathf.Pow(r3, 2) * z2 - Mathf.Pow(r3, 2) * zc * Mathf.Cos(theta3) + Mathf.Pow(r3, 2) * zc + Mathf.Pow(y2, 2) * z2 - 2 * y2 * zc * z2 + Mathf.Pow(zc, 2) * z2 + Mathf.Pow(z2, 3) - 2 * Mathf.Pow(z2, 2) * zc + z2 * Mathf.Pow(zc, 2)) / (Mathf.Pow(y2, 2) - 2 * y2 * zc + Mathf.Pow(zc, 2) + Mathf.Pow(z2, 2) - 2 * z2 * zc + Mathf.Pow(zc, 2));

        //if (yzOrient <= 360 /*180*/ && yzOrient > 180)
        if ((yzOrient > 180 && yzOrient <= 360) || (yzOrient < 0 && yzOrient >= -180))
        {
            //float diff = zc - z3;
            //z3 = zc + diff;

            float diff = Mathf.Abs(yc - y3);
            //Debug.Log("y3 BEFORE = " + y3);
            y3 = yc + diff;
            //Debug.Log("y3 AFTER = " + y3);
        }

        Debug.Log($"R3: {r3}, Theta3: {theta3}, X3: {x3}, Y3: {y3}, Z3: {z3}");

        newPos.x = x3;
        newPos.y = y3;
        newPos.z = z3;

        //Printing out stuff
        //Debug.Log("Rover Pos: " + objPos * 1000);
        //Debug.Log("Rover PoI: " + objPoIOffset * 1000);
        //Debug.Log("Rover PoI Pos (satellite): " + objPoIPos * 1000);
        //Debug.Log("Hologram Pos: " + hologramPos * 1000);

        Vector3 difference = newPos - objCenterPos;

        //Debug.Log("newOffset - objPos = difference: " + difference * 1000);

        return difference;
    }

    List<float> ParseOrientationData(string s)
    {
        // Parses the orientation received from the server into rotations about the
        // X, Y, and Z axes and puts them in a List for another function
        List<float> orients = new List<float>();
        char[] sep = new char[] { ' ', '[', ']', ',' };
        string[] arr = s.Split(sep, System.StringSplitOptions.RemoveEmptyEntries);
        foreach (var word in arr)
        {
            float o = float.Parse(word);
            orients.Add(o);
            //Debug.Log(o);
        }
        return orients;

    }
}
