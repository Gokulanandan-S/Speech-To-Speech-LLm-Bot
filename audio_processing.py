import os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import io
import re


# Directory to store voice files
VOICE_DIR = "data/voice/"
if not os.path.exists(VOICE_DIR):
    os.makedirs(VOICE_DIR)

def text_to_audio(text, filename):
    """
    Converts input text to an audio file using gTTS and saves it.
    Removes Markdown formatting before converting to speech.
    """
    try:
        # Remove Markdown syntax
        clean_text = re.sub(r'(\*{1,2}|_+|~+|`+)', '', text)
        
        # Convert cleaned text to speech
        tts = gTTS(clean_text)
        file_path = os.path.join(VOICE_DIR, filename)
        tts.save(file_path)
        return file_path
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
    
def play_audio(file_path):
    """
    Plays an audio file if it exists.
    """
    if os.path.exists(file_path):
        try:
            playsound(file_path)
        except Exception as e:
            print(f"Error playing audio: {e}")
    else:
        print(f"Audio file not found: {file_path}")

def audio_to_text(audio_binary):
    recognizer = sr.Recognizer()
    try:
        # Convert binary audio to file-like object
        audio_file = io.BytesIO(audio_binary)
        with sr.AudioFile(audio_file) as source:
            print("Recording detected, processing...")
            audio_data = recognizer.record(source)
        # Perform speech-to-text conversion
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Could not process audio due to a service issue."
    except Exception as e:
        return f"Unexpected error: {e}"

def record_audio():
    """
    Records audio from the microphone. Returns the audio object.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Recording. Speak now!")
            audio = recognizer.listen(source)
            print("Recording complete.")
            return audio
    except Exception as e:
        print(f"Error during recording: {e}")
        return None
