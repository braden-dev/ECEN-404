using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Windows.Speech;
using Vuforia;

//only one Model Target can be active at one time, so this code is used to switch between them by activing/deactiving them
public class SwitchModelTargets : MonoBehaviour
{
    private KeywordRecognizer keywordRecognizerSwitchToRover;
    private KeywordRecognizer keywordRecognizerSwitchToOther;
    GameObject rover;
    GameObject octagon;

    // Start is called before the first frame update
    void Start()
    {
        List<string> keywordRover = new List<string>();
        List<string> keywordOctagon = new List<string>();
        keywordRover.Add("Rover");
        keywordOctagon.Add("Octagon");
        keywordRecognizerSwitchToRover = new KeywordRecognizer(keywordRover.ToArray());
        keywordRecognizerSwitchToOther = new KeywordRecognizer(keywordOctagon.ToArray());
        keywordRecognizerSwitchToRover.Start();
        keywordRecognizerSwitchToOther.Start();

        rover = GameObject.Find("ModelTargetVikingRover");
        octagon = GameObject.Find("ModelTargetOctagon");
    }

    private void KeywordRecognizer_OnPhraseRecognizedSwitchToRover(PhraseRecognizedEventArgs args)
    {
        octagon.GetComponent<ModelTargetBehaviour>().enabled = false;
        rover.GetComponent<ModelTargetBehaviour>().enabled = true;

    }

    private void KeywordRecognizer_OnPhraseRecognizedSwitchToOther(PhraseRecognizedEventArgs args)
    {
        rover.GetComponent<ModelTargetBehaviour>().enabled = false;
        octagon.GetComponent<ModelTargetBehaviour>().enabled = true;
    }

    public void Update()
    {
        keywordRecognizerSwitchToRover.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognizedSwitchToRover;
        keywordRecognizerSwitchToOther.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognizedSwitchToOther;
    }
}
