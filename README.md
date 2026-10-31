Study & Focus Companion

Transform overwhelming text into concise summaries and actionable flashcards in seconds.

Team Members:  Milan Bennett, Shaheer Mohmand


1. Pitch, Problem, and Solution

 The Problem

Students and researchers face an overwhelming volume of digital text daily—from dense textbooks to lengthy lecture transcripts. Manually sifting through pages to summarize key ideas and create flashcards takes hours, causing mental fatigue before actual studying even begins.

The Solution

The Study & Focus Companion automates study preparation. Users simply paste their text into a clean web interface to instantly receive a clear summary and ready-to-use active-recall flashcards. By eliminating manual formatting and note-taking, the app saves hours of prep time and lets students focus entirely on learning.

 2. Technical Details & Hackathon Pivot

Tech Stack

Backend: Python (Flask)

AI Integration: Google GenAI SDK

Frontend: HTML5, CSS3, JavaScript

Security: python-dotenv with .env and .gitignore integration

 Optimization & Security

Model Speed & Efficiency: During the hackathon, we noticed that newer LLM models were quite slow when generating both summaries and flashcards together. To make the app fast and efficient for users, we pivoted to a lighter, reliable model that processes text much quicker without sacrificing quality.

Security & Offline Fallback: Access keys are safely stored in local environment variables and hidden from public repositories. If a key is missing or disconnected, app.py seamlessly switches to a local mock mode so the application never crashes during live testing or judging.

Future Roadmap

While built within hackathon constraints, potential future enhancements include:

Infrastructure: Deploying on dedicated cloud hosting for higher availability.

Customization: Allowing users to choose the exact count and difficulty of flashcards.

UI & Export: Adding enhanced graphic themes and export options (PDF / Anki).
