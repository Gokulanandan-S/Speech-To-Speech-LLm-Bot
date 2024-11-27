import streamlit as st
from audio_recorder_streamlit import audio_recorder
from llm_interaction import generate_response
from audio_processing import text_to_audio, audio_to_text
import os

# Directory for saving audio files
VOICE_DIR = "data/voice/"
os.makedirs(VOICE_DIR, exist_ok=True)


# Initialize the app
def main():
    st.title("💬 Voice-Based AI Assistant")
    st.write(f"**Assistant:** Hello! I'm your voice assistant. Ask me anything.")
 
    st.session_state["messages"] = [
            {"role": "Assistant", "content": "Hello! I'm your voice assistant. Ask me anything."}
        ]
    with st.container():
            user_input_init = st.empty()
            bot_input_init = st.empty()
            audio_file_init = st.empty()

    # Add audio recorder button
    recording = audio_recorder(text="Record Your Question", icon_size="2x",pause_threshold=5.0,)

    if recording:
        # Convert audio to text
        user_text = audio_to_text(recording)

        if user_text:
            # Add user message
            user_input_init.write(f"**User:** {user_text}")
            st.session_state["messages"].append({"role": "user", "content": user_text})

            # Generate bot response
            response_text = generate_response(user_text)
            st.session_state["messages"].append({"role": "system", "content": response_text})
            bot_input_init.write(f"**Assistant:** {response_text}")
            # Convert response to audio and play
            audio_file = text_to_audio(response_text, "response.mp3")
            if audio_file:
                audio_file_init.audio(audio_file, format="audio/mp3", autoplay=True)
            else:
                st.error("Failed to generate audio response.")
        else:
            st.error("Could not process audio input.")

if __name__ == "__main__":
    main()