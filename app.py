import requests
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import os
from dotenv import load_dotenv

# ✅ .env file से API key लोड करें
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ✅ Dash App Layout
app = dash.Dash(__name__)
app.title = "Groq ChatBot"

app.layout = html.Div([
    html.H1("🤖 Groq ChatBot (LLaMA3)", style={"textAlign": "center"}),

    dcc.Textarea(
        id='chat-history',
        value='',
        style={'width': '100%', 'height': 300},
        readOnly=True
    ),

    dcc.Input(
        id='user-input',
        type='text',
        placeholder='Type your message...',
        style={'width': '80%', 'marginRight': '10px'}
    ),

    html.Button('Send', id='send-button'),
])


@app.callback(
    Output('chat-history', 'value'),
    Input('send-button', 'n_clicks'),
    State('user-input', 'value'),
    State('chat-history', 'value'),
    prevent_initial_call=True
)
def chat_with_ai(n_clicks, user_input, chat_history):
    if not user_input:
        return chat_history

    data = {
        "model": "llama3-8b-8192",  # ✅ Working Groq Model
        "messages": [{"role": "user", "content": user_input}]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        chat_history += f"\nतुम: {user_input}\nAI: {reply.strip()}\n"
    else:
        chat_history += f"\n❌ Error {response.status_code}: {response.text}\n"

    return chat_history


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
