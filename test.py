import os, time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.6-flash"
TEXT = "Summarize in one sentence: The mitochondria is the powerhouse of the cell."

def run(label, **kwargs):
    start = time.time()
    client.models.generate_content(model=MODEL, contents=TEXT, **kwargs)
    print(f"{label}: {time.time() - start:.1f}s")

run("plain")
run("json mode", config=types.GenerateContentConfig(response_mime_type="application/json"))