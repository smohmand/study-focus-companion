"""
File: app.py
Project: Study & Focus Companion
Description: Flask backend handling server routing with optional Gemini AI integration.
Author(s):  Git Push and Pray (Milan Bennett, Shaheer Mohmand)
Date: October 2026
"""
import sys
import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# SWITCH TO FALSE WHEN HOSTED, TRUE FOR TESTING
DEV_MODE = True

# Load local environment variables if a .env file exists
load_dotenv()

# Safely check for the Gemini API key without crashing if it's missing
API_KEY = os.getenv("GEMINI_API_KEY")
client = None


print("Python being used:", sys.executable)
print("Key found:", API_KEY is not None)

if API_KEY:
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        if DEV_MODE == True:
            print(f"GenAI SDK not initialized: {e}")

# Initialize Flask with template and static folders mapped to the root directory
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# ==========================================
# ROUTING LOGIC
# ==========================================

@app.route('/process-text', methods=['POST'])
def process_text():
    data = request.get_json() if request.is_json else {}
    user_text = data.get('text', '').strip()

    if not user_text:
        return jsonify({'summary': 'Please provide text.', 'flashcards': []})

    mock_reason = "no API key or SDK not initialized"

    # If the Gem client is initialized, use the real LLM
    if client:
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
                model='gemini-3.8-flash',
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
            print(f"Gemini API error: {e}")
            mock_reason = f"Gemini error: {e}"

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

# Run the local development server
if __name__ == '__main__':
    app.run(debug=DEV_MODE, port=5381)