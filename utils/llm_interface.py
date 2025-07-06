import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup OpenAI client (new API v1.0+)
try:
    import openai
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    client = None

def send_prompt_to_llm(user_input, persona="", backend="openai"):
    """
    Route prompt to selected backend: 'openai' or 'ollama'
    """
    if backend == "ollama":
        return send_to_ollama(user_input, persona)
    else:
        return send_to_openai(user_input, persona)

def send_to_openai(user_input, persona=""):
    """
    Send prompt to OpenAI using new SDK (v1.0+)
    """
    if client is None:
        return "❌ OpenAI SDK not available. Make sure 'openai' package is installed."

    messages = []
    if persona:
        messages.append({"role": "system", "content": persona})
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ OpenAI error: {str(e)}"

def send_to_ollama(user_input, persona=""):
    """
    Send prompt to local Ollama server running gemma:3b model
    """
    prompt = f"{persona.strip()}\n\nUser: {user_input}" if persona else user_input
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma3:latest", "prompt": prompt, "stream": False}
        )
        if response.ok:
            return response.json().get("response", "").strip()
        else:
            return f"❌ Ollama error: {response.text}"
    except Exception as e:
        return f"❌ Ollama connection failed: {str(e)}"
