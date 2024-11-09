import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def text_to_speech(text_list):
    text = " ".join(text_list)
    engine.say(text)
    engine.runAndWait()