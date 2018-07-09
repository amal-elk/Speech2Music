import random
import time
import speech_recognition as sr
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
import json
import pygame


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("say something...")
    guess = recognize_speech_from_mic(recognizer, microphone)


        # show the user the transcription
    print("You said: {}".format(guess["transcription"]))

    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        username='97253202-3e7e-4e86-9c20-1cb0581c9b4e',
        password='ieJUCcp32UMN'
      #  url = 'https://gateway.watsonplatform.net/tone-analyzer/api'
    )

    text = guess["transcription"]
    content_type = 'application/json'
    #print(text)
    tone = tone_analyzer.tone({"text": text},content_type)
    tones = tone["document_tone"]["tones"]

    tones_detected = {}
    for tone in tones:
        score = tone["score"]
        tone_name = tone["tone_name"]
        print("Tone Detected ({}): {}".format(tone_name, str(score*100.0)))
        tones_detected[tone_name] = score

    main_tone = list(reversed(sorted(tones_detected, key=tones_detected.get)))[0]
    print("Main tone detected: ", main_tone)

    if(main_tone == "Confident" or main_tone == "Tentative" or main_tone == "Analytical"):
        print(list(reversed(sorted(tones_detected, key=tones_detected.get)))[1])
        main_tone = list(reversed(sorted(tones_detected, key=tones_detected.get)))[1]

    pygame.init()
    pygame.mixer.init()

    if(main_tone == "Joy"):
        print("Playing happy song")
        pygame.mixer.music.load("happy.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.quit()
        print ("done")

    elif(main_tone == "Sadness"):
        print("Playing sad song")
        pygame.mixer.music.load("sad.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.quit()
        print ("done")
        
    elif(main_tone == "Fear"):
        print("Playing fearful song")
        pygame.mixer.music.load("fear.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.quit()
        print ("done")

    elif(main_tone == "Anger"):
        print("Playing angry song")
        pygame.mixer.music.load("angry.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.quit()
        print ("done")



