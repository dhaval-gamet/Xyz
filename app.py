from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json as pyjson
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
CORS(app)

API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "🧠 Groq Excel AI API is Running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # 🧠 System Prompt to instruct LLaMA AI
    system_msg = (
        "You are an intelligent Excel assistant AI. "
        "The user will describe tasks in natural language, like: "
        "'Write Total in A1', 'Set A2 to 500', 'Highlight B3', or "
        "'Fill A1 to A5 with names'. "
        "Your job is to convert this into a list of actions in JSON format like:\n\n"
        "["
        "{\"cell\": \"A1\", \"value\": \"Total\", \"highlight\": true}, "
        "{\"cell\": \"A2\", \"value\": \"500\"}, "
        "{\"cell\": \"A3\", \"value\": \"=A1+A2\"} "
        "]\n\n"
        "Only return the JSON list. No explanation, no markdown. Only pure JSON array."
    )

    api_payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt}
        ]
    }

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
        reply = res.json()["choices"][0]["message"]["content"].strip()

        try:
            actions = pyjson.loads(reply)
            return jsonify({"actions": actions})
        except Exception as e:
            return jsonify({"response": reply})  # fallback simple response

    except requests.exceptions.Timeout:
        return jsonify({"error": "Groq API timeout"}), 504
    except Exception as e:
        return jsonify({"error": "Groq API failed", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)