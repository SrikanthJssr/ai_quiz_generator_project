from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Local imports (already implemented by you earlier)
from scraping import extract_text_from_wiki
from quiz_generator import generate_quiz


# FastAPI App Instance
app = FastAPI(
    title="DeepKlarity - AI Wiki Quiz Generator",
    description="Backend API for generating quizzes from Wikipedia URLs.",
    version="1.0.0"
)


# Allow Frontend (React/Streamlit/HTML) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all frontend domains for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Model
class URLRequest(BaseModel):
    url: str


# Root Endpoint (Health Check)
@app.get("/")
def home():
    return {"status": "✅ API Running Successfully", "message": "Use /extract or /generate_quiz"}


# STEP 1: Extract Wikipedia Text Only
@app.get("/extract")
def extract(url: str):
    """
    Input: Wikipedia URL
    Output: Cleaned article text (summary format)
    """
    text = extract_text_from_wiki(url)

    if not text:
        return {"error": "❌ Could not extract content. Check URL."}

    # Return clean extracted content (Used in TAB-1)
    return {
        "url": url,
        "content_preview": text[:600] + "...",  # to avoid sending huge text
        "full_content": text
    }


# STEP 2: Generate Quiz using LLM
@app.post("/generate_quiz")
def generate(data: URLRequest):
    """
    Input: Wikipedia URL
    Output: Quiz JSON = Questions, Options, Answers, Difficulty, Explanation, Related Topics
    """
    url = data.url
    text = extract_text_from_wiki(url)

    if not text:
        return {"error": "❌ Unable to fetch article text."}

    quiz_data = generate_quiz(text)  # this will be LLM powered next

    return {
        "url": url,
        "quiz_count": len(quiz_data),
        "quiz": quiz_data
    }


# MAIN Runner
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
