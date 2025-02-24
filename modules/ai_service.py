import os
import requests
from dotenv import load_dotenv
from modules.database import save_message, get_conversation

# Load API Key
#load_dotenv()
#MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_KEY = "4vrJkd3Aik0zhPjfUgzEWw0xzjhCjbYE"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def get_mistral_response(user_input, session_id):
    """Fetch AI response from Mistral, considering past chat history."""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Retrieve previous conversation
    conversation_history = get_conversation(session_id)
    
    messages = [{
        "role": "system",
        "content": "You are an advanced AI assistant designed to provide users with accurate and comprehensive information. Your goal is to assist users in finding relevant and up-to-date information while maintaining conversation history."
    }]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "mistral-medium",
        "messages": messages,
        "max_tokens": 2000
    }

    response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        bot_response = response.json()["choices"][0]["message"]["content"]
        save_message(session_id, "user", user_input)
        save_message(session_id, "assistant", bot_response)
        return bot_response
    return "Error: Unable to fetch response."