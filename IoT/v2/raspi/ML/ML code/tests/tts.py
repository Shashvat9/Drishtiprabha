# test_tts.py
import sys
sys.path.append("IoT/v2/raspi/ML/ML\ code/text_to_speech.py")
from text_to_speech import text_to_speech

def test_tts():
    sample_text = ["This is a test of the text to speech system."]
    text_to_speech(sample_text)

if __name__ == "__main__":
    test_tts()