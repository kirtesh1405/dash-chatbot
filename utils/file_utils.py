import os
import json
import uuid
from datetime import datetime
from utils.summarizer import generate_summary

CHATS_DIR = os.path.join("data", "chats")
os.makedirs(CHATS_DIR, exist_ok=True)

def generate_chat_id():
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

def save_chat_to_file(messages, chat_id=None):
    if not chat_id:
        chat_id = generate_chat_id()
    file_path = os.path.join(CHATS_DIR, f"{chat_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)
    
    return chat_id

def load_all_chats():
    chats = []
    for filename in sorted(os.listdir(CHATS_DIR), reverse=True):
        if filename.endswith(".json"):
            chat_id = filename.replace(".json", "")
            path = os.path.join(CHATS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                messages = json.load(f)
            chats.append((chat_id, messages))
    return chats

def summarize_chat(messages, backend="openai"):
    return generate_summary(messages, backend)
