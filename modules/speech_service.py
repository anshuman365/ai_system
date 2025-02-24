import os
from gtts import gTTS

def text_to_speech(text):
    # Ensure the static/audio directory exists
    audio_dir = 'static/audio'
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    file_path = os.path.join(audio_dir, 'output.mp3')
    
    # Convert text to speech and save the audio file
    tts = gTTS(text)
    tts.save(file_path)
    
    return file_path  # Return the path for further use in the frontend