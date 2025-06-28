from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Groq Flask API is running!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    user_input = data.get("message")
    if not user_input:
        return jsonify({"error": "Missing 'message' in JSON body"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply.strip()})
    else:
        return jsonify({"error": "Groq API Error", "details": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)