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
    data = request.json
    messages = data.get("messages")
    user_msg = data.get("message", "")

    if messages:
        # अगर messages (multi-turn) है तो उसे Groq को भेजो
        api_payload = {
            "model": "llama3-8b-8192",
            "messages": messages
        }
    elif user_msg:
        # single message (single-turn)
        api_payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": user_msg}]
        }
    else:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=api_payload,
            timeout=20
        )
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply.strip()})
    except requests.exceptions.Timeout:
        return jsonify({"error": "Groq API timeout"}), 504
    except Exception as e:
        return jsonify({"error": "Groq API failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)