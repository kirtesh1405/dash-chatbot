# 🧠 Dash Chatbot Application Documentation

## 📁 Project Structure

```
dash_chatbot/
├── app.py                          # Main Dash app entry point
├── callbacks/
│   └── chat_callbacks.py           # All app callbacks and logic
├── components/
│   └── layout.py                   # UI layout using class-based styling
├── utils/
│   ├── file_utils.py              # Chat save/load, summary generation
│   ├── llm_interface.py           # OpenAI + Ollama backend logic
│   └── summarizer.py              # LLM-powered summary helper
├── data/
│   └── chats/                     # Saved chat JSON files
├── assets/
│   └── styles.css                 # All CSS for UI elements
├── .env                           # API key for OpenAI
└── requirements.txt               # Python dependencies
```

---

## 📦 Dependencies

```bash
pip install dash openai requests python-dotenv
```

---

## 🧩 Main Features

* Sidebar with "New Chat" and summarized chat history
* Backend model switch (OpenAI GPT-3.5 or local Ollama Gemma)
* Persona input to define LLM behavior
* Markdown support in responses
* Auto-saving and reloading chats with summaries
* Clean CSS-driven layout

---

## 🔧 Detailed Code Description

### `app.py`

* Loads layout from `components/layout.py`
* Registers callbacks from `chat_callbacks.py`
* Starts the server on custom host/port

```python
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.42', port=8055)
```

---

### `layout.py`

* Defines the two-pane layout:

  * Left 20%: Sidebar with new chat + summaries
  * Right 80%: Dropdown, persona, chat, input area
* Uses class-based styling only (no inline styles)

---

### `styles.css`

* Applies styles to layout elements
* Controls:

  * Background: black
  * Borders: red
  * Buttons: yellow
  * Text: white
* Dropdown hover and menu styled with custom CSS

---

### `chat_callbacks.py`

* Unified callback handles:

  * Sending message
  * Starting new chat
  * Loading chat history
* Secondary callback updates model label below dropdown
* Uses `.children` fallback for safely extracting structured messages

---

### `llm_interface.py`

* Chooses between:

  * OpenAI GPT-3.5 using new SDK (`openai.OpenAI()`)
  * Ollama local model using HTTP call to `localhost:11434`
* Loads `OPENAI_API_KEY` from `.env`

---

### `file_utils.py`

* Saves chat to JSON file
* Loads all chat history
* Summarizes conversations using OpenAI or Ollama

---

### `summarizer.py`

* Simple wrapper to send summarization prompts to backend

---

## 👤 User Flow Summary

### User Actions:

1. Launches the app → Sees sidebar and chat UI
2. Selects a model (OpenAI / Ollama)
3. Defines the persona (optional)
4. Starts typing chat
5. LLM replies with formatted response
6. Chat is saved + one-liner summary appears in sidebar
7. User clicks any old summary → Chat is restored
8. Clicks "New Chat" → Chat area is reset

---

## 🔄 Chatbot Flow Chart

```text
[User Input] --> [Send Button]
    --> [Select Backend + Persona]
    --> [send_prompt_to_llm()]
    --> [OpenAI or Ollama API]
    --> [LLM Response]
    --> [Chat Display Updated]
        --> [Save to JSON + Generate Summary]
        --> [Sidebar Updated with Summary]

[Click Summary] --> [Load Chat from JSON]
[Click New Chat] --> [Clear Chat + Reset Persona]
```

---

## ✅ Next Steps (Optional Enhancements)

* Add export/download chat button
* Add avatars or chat bubbles
* Add mobile responsiveness
* Add support for Claude, Mistral, Gemini, etc.
* Add streaming/token-based response handling
