import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not set in .env")

genai.configure(api_key=GEMINI_KEY)

MODEL_NAME = "models/gemini-2.5-flash"   # ✅ Correct model

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "quiz_prompt.txt"


def _extract_json_from_text(text: str):
    """Extract JSON safely from model output."""
    try:
        return json.loads(text)
    except:
        pass

    # Try { ... }
    m = re.search(r"(\{[\s\S]*\})", text)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            pass

    # Try [ ... ]
    m2 = re.search(r"(\[[\s\S]*\])", text)
    if m2:
        try:
            return json.loads(m2.group(1))
        except:
            pass

    raise ValueError("❌ Could not parse JSON from LLM output")


def generate_quiz_from_text(title: str, article_text: str):
    """Generate quiz JSON from Wikipedia text using Gemini."""
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{article_text}", article_text)

    model = genai.GenerativeModel(MODEL_NAME)

    response = model.generate_content(prompt)
    text = response.text if hasattr(response, "text") else str(response)

    obj = _extract_json_from_text(text)

    # Normalize format
    if isinstance(obj, dict):
        obj.setdefault("title", title)
    else:
        obj = {"title": title, "quiz": obj}

    return obj