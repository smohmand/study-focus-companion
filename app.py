"""
File: app.py
Project: Study & Focus Companion
Description: Flask backend handling server routing with optional Gemini AI integration.
Author(s):  Git Push and Pray (Milan Bennett, Shaheer Mohmand)
Date: October 2026
"""
import os
import json
import time
from datetime import date
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter

import time
from werkzeug.serving import WSGIRequestHandler

class TimedHandler(WSGIRequestHandler):
    def run_wsgi(self):
        self._start = time.time()
        super().run_wsgi()

    def log_request(self, code="-", size="-"):
        elapsed = time.time() - getattr(self, "_start", time.time())
        super().log_request(code, f"{size} ({elapsed:.2f}s)")

load_dotenv()

# Off by default. Only set DEV_MODE=true in your local .env, never on Render
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

MAX_INPUT_CHARS = 8000
DAILY_CAP = 300
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

API_KEY = os.getenv("GEMINI_API_KEY")
client = None

if API_KEY:
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"GenAI SDK not initialized: {e}" if DEV_MODE else "GenAI SDK not initialized")
else:
    print("No GEMINI_API_KEY found, running in basic mode")

app = Flask(__name__)


def client_ip():
    # Render sits behind a proxy, so the real visitor IP is in X-Forwarded-For
    forwarded = request.headers.get("X-Forwarded-For", "")
    return forwarded.split(",")[0].strip() or request.remote_addr or "unknown"


limiter = Limiter(client_ip, app=app, default_limits=[])

usage = {"day": date.today(), "count": 0}


def over_daily_cap():
    today = date.today()
    if usage["day"] != today:
        usage["day"] = today
        usage["count"] = 0
    usage["count"] += 1
    return usage["count"] > DAILY_CAP


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process-text', methods=['POST'])
@limiter.limit("5 per minute")
def process_text():
    data = request.get_json(silent=True) or {}
    user_text = str(data.get('text', '')).strip()

    if not user_text:
        return jsonify({'summary': 'Please provide text.', 'flashcards': []})

    user_text = user_text[:MAX_INPUT_CHARS]
    mock_reason = "no API key or SDK not initialized"

    if client and over_daily_cap():
        mock_reason = "demo limit reached for today"
    elif client:
        try:
            prompt = f"""
            Analyze the following text and provide:
            1. A concise summary.
            2. Three key Q&A flashcards based on the text.

            You must format your response strictly as a JSON object with two keys:
            - "summary": a string containing the summary.
            - "flashcards": a list of objects, where each object has a "question" and "answer" key.

            Text to analyze: {user_text}
            """

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )

            result = json.loads(response.text)
            return jsonify({
                'summary': result.get('summary', 'Summary unavailable.'),
                'flashcards': result.get('flashcards', [])
            })

        except Exception as e:
            print(f"Gemini API error: {e}")  # stays in server logs
            mock_reason = f"Gemini error: {e}" if DEV_MODE else "AI temporarily unavailable"

    # --- FALLBACK MODE ---
    sentences = [s.strip() for s in user_text.split('.') if s.strip()]
    summary = ". ".join(sentences[:2]) + "." if sentences else "Summary unavailable."

    flashcards = [
        {
            "question": "What core event or milestone is described?",
            "answer": sentences[0] if sentences else "N/A"
        },
        {
            "question": "What text metrics were analyzed?",
            "answer": f"{len(user_text)} characters across {len(sentences)} sentences."
        },
        {
            "question": "What is the primary conclusion or takeaway?",
            "answer": sentences[-1] + "." if len(sentences) > 1 else "Core historical achievement."
        }
    ]

    return jsonify({
        'summary': f"[Mock Mode - {mock_reason}] {summary}",
        'flashcards': flashcards
    })

    return jsonify({
        'summary': f"[Basic Mode - {mock_reason}] {summary}",
        'flashcards': flashcards
    })


if __name__ == '__main__':
    app.run(debug=DEV_MODE, port=5381, request_handler=TimedHandler)