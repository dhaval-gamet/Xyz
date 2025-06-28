# 🤖 Groq ChatBot (Dash UI)

यह एक Open Source ChatBot है जो Groq के LLaMA3 मॉडल को यूज़ करता है।

## Features
- Fast AI response (Groq API)
- Built with Python + Dash
- Free Render hosting
- Secure API key via `.env` or Render Env Vars

## How to Run (Locally)
1. `pip install -r requirements.txt`
2. `.env` में API key डालो
3. `python app.py`

## Deploy to Render
1. GitHub पर ये फाइलें डालो
2. Render में "New Web Service" ➝ GitHub Repo सिलेक्ट करो
3. Env Vars में `GROQ_API_KEY` जोड़ो
4. Deploy और Enjoy!