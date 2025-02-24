from flask import Flask, render_template, request, jsonify
from modules.ai_service import get_mistral_response
from modules.speech_service import text_to_speech  # Remove speech_to_text if not needed
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    session_id = data.get("session_id", str(uuid.uuid4()))  # Generate session ID if not provided

    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    ai_response = get_mistral_response(user_input, session_id)
    audio_url = text_to_speech(ai_response)  # Convert AI response to speech
    return jsonify({"response": ai_response, "audio_url": audio_url, "session_id": session_id})

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_api():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    print(f"Received audio file: {audio_file.filename}")  # Debugging log

    text = speech_to_text(audio_file)
    ai_response = get_mistral_response(text, str(uuid.uuid4()))  # Send recognized text to AI
    audio_url = text_to_speech(ai_response)  # Convert AI response to speech
    return jsonify({"text": text, "audio_url": audio_url, "response": ai_response})

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech_api():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    audio_url = text_to_speech(text)
    return jsonify({"audio_url": audio_url})

if __name__ == '__main__':
    app.run(debug=True)