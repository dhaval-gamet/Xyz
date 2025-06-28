from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
CORS(app) 

API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "🧠 Groq Chatbot API is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    if not user_msg:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": user_msg}]
    }

    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if res.status_code == 200:
        reply = res.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply.strip()})
    else:
        return jsonify({"error": "Groq API failed", "details": res.text}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)