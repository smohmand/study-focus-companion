"""
File: app.py
Project: Study & Focus Companion
Description: Flask backend handling server routing and text processing logic for summaries and flashcards.
Author: Hackathon Team(Shaheer Mohmand, Milan Bennett, Driss Jouhari)
Date: October 2026
"""
import os
from flask import Flask, render_template, request, jsonify



app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

# ==========================================
# ROUTING LOGIC
# ==========================================

@app.route('/')
def home():
    """
    Renders the main frontend dashboard (index.html).
    """
    return render_template('index.html')

# ==========================================
# API ENDPOINTS
# ==========================================

@app.route('/process-text', methods=['POST'])
def process_text():
    """
    Endpoint: /process-text
    Method: POST
    Description: Receives raw study text from the frontend, generates 
                 a brief summary, and builds interactive flashcards.
    """
    data = request.get_json()
    user_text = data.get('text', '')
    
    # Core logic: Generate a summarized snippet and mock flashcards
    summary = f"Summary of text: {user_text[:100]}..."
    flashcards = [
        {"question": "What is the main topic?", "answer": user_text[:30] + "..."},
        {"question": "Key takeaway?", "answer": "Active learning saves time."}
    ]
    
    return jsonify({
        'summary': summary,
        'flashcards': flashcards
    })

# Run the local development server
if __name__ == '__main__':
    app.run(debug=True)