from dash import Dash
from components.layout import serve_layout
from callbacks.chat_callbacks import register_callbacks

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    title='Dash ChatGPT',
    update_title=None
)

app.layout = serve_layout()
register_callbacks(app)

if __name__ == '__main__':
    app.run(
        debug=False,                    
        port=8055           # Custom port
    )
