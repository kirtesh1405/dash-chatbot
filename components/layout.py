from dash import html, dcc

def serve_layout():
    return html.Div(
        style={'display': 'flex', 'height': '100vh'},
        children=[

            # Sidebar (Left Panel)
            html.Div(
                className='sidebar',
                children=[
                    html.Button('New Chat', id='new-chat-btn'),
                    html.Div(id='chat-summary-list')
                ]
            ),

            # Main Chat Area (Right Panel)
            html.Div(
                className='main-panel',
                children=[

                    # Dropdown + Label
                    html.Div([
                        dcc.Dropdown(
                            id='backend-selector',
                            options=[
                                {'label': 'OpenAI GPT-3.5', 'value': 'openai'},
                                {'label': 'Local Ollama (Gemma 3B)', 'value': 'ollama'}
                            ],
                            value='openai',
                            clearable=False
                        ),
                        html.Div(id='backend-label')
                    ]),

                    # Persona Input
                    dcc.Textarea(
                        id='persona-input',
                        placeholder='Define LLM persona here...'
                    ),

                    # Chat Display Area
                    html.Div(id='chat-display'),

                    # Input Panel (user input + send)
                    html.Div(
                        className='input-panel',
                        children=[
                            dcc.Input(
                                id='user-input',
                                type='text',
                                placeholder='Type your message...'
                            ),
                            html.Button('Send', id='send-btn', n_clicks=0)
                        ]
                    )
                ]
            )
        ]
    )
