import os
import numpy as np
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from audio_recorder_streamlit import audio_recorder

# Load environment variables
genai.configure(api_key='AIzaSyAqxAc7QMhVS190bcWgQd6XTHKsqIjx1S4')

# Path to store voice files
path = "../data/voice/"
os.makedirs(path, exist_ok=True)

# Function to convert text to audio
def text_to_audio(text, filename):
    tts = gTTS(text)
    file_path = os.path.join(path, filename)
    tts.save(file_path)
    return file_path

# Function to play audio
def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)

# Function to record audio
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording...")
        recorded_audio = recognizer.listen(source)
        print("Done recording.")
    return recorded_audio

# Function to convert audio to text
def audio_to_text(audio):
    recognizer = sr.Recognizer()
    try:
        print("Recognizing the text...")
        text = recognizer.recognize_google(audio)
        print("Decoded Text: {}".format(text))
    except sr.UnknownValueError:
        text = "Could not understand the audio."
    except sr.RequestError:
        text = "Could not request results from the service."
    return text

# Function to synthesize speech from text
def text_to_speech(text):
    tts = gTTS(text)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
    play(audio_segment)

# Function to handle voice-to-voice interaction
def voice_to_voice():
    recorded_audio = record_audio()
    text = audio_to_text(recorded_audio)
    text_to_speech(text)

# Streamlit interface
def main():
    st.title("Voice-to-Voice LLM Assistant")
    
    if st.button("Record and Get Response"):
        st.write("Listening...")
        voice_to_voice()
        st.write("Done.")

if __name__ == "__main__":
    main()