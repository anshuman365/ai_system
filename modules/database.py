conversation_data = {}

def save_message(session_id, role, message):
    if session_id not in conversation_data:
        conversation_data[session_id] = []
    conversation_data[session_id].append({"role": role, "content": message})

def get_conversation(session_id):
    return conversation_data.get(session_id, [])