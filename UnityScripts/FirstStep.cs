using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Vuforia;

//Used for button together the two halves of the birdhouse
public class FirstStep : MonoBehaviour
{

    GameObject BH, bhPerch, bhPerchDesiredPos, bhPerchDesiredPos2, bhPerchOutline, mainCam, bhCenter, IdentifyPeg, nextButton, nextButtonPos;
    Vector3 bhFrontPos, bhBackPos;

    public Vector3 newOffsetFromHD = new Vector3(0.0f, 0.0f, 0.0f);

    public List<float> rotChange;
    bool goOnce, keepGoing, keepMoving, identified;

    // Start is called before the first frame update
    void Start()
    {
        BH = GameObject.Find("ModelTargetBirdHouse");
        bhPerch = GameObject.Find("ModelTargetBirdHousePerch");
        bhPerchDesiredPos = GameObject.Find("bhPerchDesiredPos");
        bhPerchDesiredPos2 = GameObject.Find("bhPerchDesiredPos2");
        bhPerchOutline = GameObject.Find("bhPerchOutline");
        mainCam = GameObject.Find("Main Camrea");
        bhCenter = GameObject.Find("BirdHouseCenter");
        IdentifyPeg = GameObject.Find("IdentifyPeg");
        nextButton = GameObject.Find("NextButton");
        nextButtonPos = GameObject.Find("NextButtonPos");

        //Debug.Log(BH.GetComponent<ModelTargetBehaviour>().enabled);
        //Debug.Log(bhPerch.GetComponent<ModelTargetBehaviour>().enabled);

        //BH.GetComponent<ModelTargetBehaviour>().enabled = true;
        //BH.GetComponent<ModelTargetBehaviour>().Reset();
        //bhPerch.GetComponent<ModelTargetBehaviour>().enabled = false;

        goOnce = true;
        keepGoing = false;
        keepMoving = true;
        identified = false;
    }

    // Update is called once per frame
    void Update()
    {
        //newOffsetFromHD = mainCam.GetComponent<FirstStepHologramDisplay>().newOffset;
        //Debug.Log("New Offset: " + mainCam.GetComponent<FirstStepHologramDisplay>().newOffset);

        if ((newOffsetFromHD.x != 0.0f) && (newOffsetFromHD.y != 0.0f) && (newOffsetFromHD.z != 0.0f))
        {
            //BH.GetComponent<ModelTargetBehaviour>().enabled = true;
            //Debug.Log("New Offset: " + newOffsetFromHD);
            if (BH.GetComponent<ModelTargetBehaviour>().TargetStatus.Status.Equals(Status.TRACKED))
            {
                //bhPerchDesiredPos.transform.position = newOffsetFromHD + bhCenter.transform.position;

                if (goOnce == true)
                {
                    goOnce = false;
                    Vector3 rotChangeVec = new Vector3(rotChange[0], rotChange[1], rotChange[2]);
                    //Debug.Log("Rotation Change Vector: " + rotChangeVec);
                    //bhPerchDesiredPos.transform.eulerAngles = bhPerchDesiredPos.transform.eulerAngles - rotChangeVec;
                    //Debug.Log("NEW Perch Euler Angle Rotation: " + bhPerchDesiredPos);
                    StartCoroutine(Wait());
                }

                if (keepGoing == true)
                {
                    BH.GetComponent<ModelTargetBehaviour>().enabled = false;
                    bhPerch.GetComponent<ModelTargetBehaviour>().enabled = true;
                }
            }
        }

        

        if (bhPerch.GetComponent<ModelTargetBehaviour>().TargetStatus.Status.Equals(Status.TRACKED))
        {
            
            if (goOnce == true)
            {
                bhPerchOutline.transform.position = bhPerch.transform.position;
                //bhPerchOutline.transform.LookAt(bhPerchDesiredPos.transform);
                bhPerchOutline.transform.rotation = bhPerchDesiredPos.transform.rotation;
                bhPerch.GetComponent<ModelTargetBehaviour>().enabled = false;
                identified = true;
                goOnce = false;
            }
        }

        if(identified == true)
        {
            bhPerchOutline.transform.position = Vector3.MoveTowards(bhPerchOutline.transform.position, bhPerchDesiredPos.transform.position, 0.002f);
            IdentifyPeg.GetComponent<MeshRenderer>().enabled = false;
            
        }
    }



    IEnumerator Wait()
    {
        bhPerchDesiredPos2.transform.position = bhPerchDesiredPos.transform.position;
        bhPerchDesiredPos2.transform.rotation = bhPerchDesiredPos.transform.rotation;
        //Debug.Log("hello");
        yield return new WaitForSeconds(10);

        keepGoing = true;
        goOnce = true;
        IdentifyPeg.GetComponent<MeshRenderer>().enabled = true;
        //bhPerchDesiredPos.transform.eulerAngles += new Vector3(0, 45, 0);
        //bhPerchDesiredPos.transform.eulerAngles = new Vector3(0, 0, 0);
        nextButton.transform.position = nextButtonPos.transform.position;
        //Debug.Log("hello pt. 2");
    }
}
