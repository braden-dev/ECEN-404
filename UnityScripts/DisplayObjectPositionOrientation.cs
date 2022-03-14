using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class DisplayObjectPositionOrientation : MonoBehaviour
{
    //public TMP_Text objRot;
    public TextMesh objRot;
    GameObject Rover;

    // Start is called before the first frame update
    void Start()
    {
        objRot = gameObject.GetComponent("TextMesh") as TextMesh;
        Rover = GameObject.Find("ModelTargetVikingRover");
        Debug.Log(Rover.transform.eulerAngles.ToString());
    }

    // Update is called once per frame
    void Update()
    {
        objRot.text = Rover.transform.eulerAngles.ToString();
        //Debug.Log(Rover.transform.eulerAngles.ToString());
    }
}
