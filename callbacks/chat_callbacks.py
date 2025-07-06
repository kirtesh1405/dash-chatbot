from dash import Input, Output, State, html, ctx, dcc, ALL
import dash
import os
import json

from utils.llm_interface import send_prompt_to_llm
from utils.file_utils import save_chat_to_file, summarize_chat, load_all_chats

CURRENT_CHAT_ID = None

def register_callbacks(app: dash.Dash):
    # 🔁 Dropdown backend label update
    @app.callback(
        Output('backend-label', 'children'),
        Input('backend-selector', 'value')
    )
    def update_backend_label(backend):
        if backend == 'openai':
            return "⚙️ Model selected: OpenAI GPT-3.5"
        elif backend == 'ollama':
            return "⚙️ Model selected: Local Ollama (Gemma 3B)"
        return ""

    # 🔁 Combined Callback for Send, New Chat, Load History
    @app.callback(
        Output('chat-display', 'children'),
        Output('persona-input', 'value'),
        Output('chat-summary-list', 'children'),
        Input('send-btn', 'n_clicks'),
        Input('new-chat-btn', 'n_clicks'),
        Input({'type': 'summary-button', 'index': ALL}, 'n_clicks'),
        State('user-input', 'value'),
        State('persona-input', 'value'),
        State('chat-display', 'children'),
        State('backend-selector', 'value'),
        prevent_initial_call=True
    )
    def handle_all_actions(send_clicks, new_clicks, summary_clicks, user_input, persona, chat_display, backend):
        global CURRENT_CHAT_ID
        triggered = ctx.triggered_id

        # ✳️ New Chat
        if triggered == 'new-chat-btn':
            CURRENT_CHAT_ID = None
            return [], "", load_chat_summaries()

        # ✳️ Load Previous Chat
        if isinstance(triggered, dict) and triggered.get('type') == 'summary-button':
            chat_id = triggered['index']
            CURRENT_CHAT_ID = chat_id
            path = os.path.join("data", "chats", f"{chat_id}.json")
            with open(path, "r", encoding="utf-8") as f:
                messages = json.load(f)

            display = []
            for m in messages:
                who = "You" if m["role"] == "user" else "Bot"
                display.append(html.Div([
                    html.Strong(f"{who}: "),
                    dcc.Markdown(m["content"], style={'whiteSpace': 'pre-wrap'})
                ], style={'marginBottom': '10px'}))

            return display, "", load_chat_summaries()

        # ✳️ Send Prompt
        if triggered == 'send-btn':
            if not user_input:
                raise dash.exceptions.PreventUpdate

            user_msg = html.Div([
                html.Strong("You: "),
                html.Span(user_input)
            ], style={'marginBottom': '5px'})

            response = send_prompt_to_llm(user_input, persona or "", backend)

            bot_msg = html.Div([
                html.Strong("Bot: "),
                dcc.Markdown(response, style={'whiteSpace': 'pre-wrap'})
            ], style={'marginBottom': '10px'})

            updated_chat = (chat_display or []) + [user_msg, bot_msg]

            # 🔍 Convert to structured message format
            messages = []
            for block in updated_chat:
                if hasattr(block, "children"):
                    children = block.children
                    if isinstance(children, list) and len(children) >= 2:
                        who = getattr(children[0], "children", "")
                        text = getattr(children[1], "children", "")
                        role = "user" if "You" in who else "assistant"
                        messages.append({"role": role, "content": text})
                elif isinstance(block, dict):
                    try:
                        who = block["props"]["children"][0]["props"]["children"]
                        text = block["props"]["children"][1]["props"]["children"]
                        role = "user" if "You" in who else "assistant"
                        messages.append({"role": role, "content": text})
                    except Exception:
                        continue

            # 💾 Save chat
            if not CURRENT_CHAT_ID:
                CURRENT_CHAT_ID = save_chat_to_file(messages)
            else:
                save_chat_to_file(messages, CURRENT_CHAT_ID)

            return updated_chat, "", load_chat_summaries()

        raise dash.exceptions.PreventUpdate

    # 🔁 Build sidebar summaries
    def load_chat_summaries():
        summary_buttons = []
        for chat_id, messages in load_all_chats():
            summary = summarize_chat(messages)
            summary_buttons.append(
                html.Button(summary, id={'type': 'summary-button', 'index': chat_id}, style={
                    'width': '100%',
                    'marginBottom': '5px',
                    'backgroundColor': 'black',
                    'color': 'white',
                    'border': '1px solid red',
                    'textAlign': 'left',
                    'padding': '5px'
                })
            )
        return summary_buttons
