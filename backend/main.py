from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scraper import extract_text_from_wiki
from llm_quiz_generator import generate_quiz_from_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizRequest(BaseModel):
    url: str

# -------------------- In-Memory History --------------------
quiz_history = []  # stores previously generated quizzes
quiz_id_counter = 1  # incremental ID for each quiz

@app.get("/")
def home():
    return {"status": "✅ Backend is running"}

@app.get("/extract")
def extract(url: str):
    title, text, extras = extract_text_from_wiki(url)
    if not text:
        raise HTTPException(400, "Could not extract article text.")
    return {"title": title, "text": text, "extras": extras}

@app.post("/generate_quiz")
def generate(req: QuizRequest):
    global quiz_id_counter
    title, text, extras = extract_text_from_wiki(req.url)
    if not text:
        raise HTTPException(400, "Could not extract text from article.")

    # Generate quiz using your existing LLM generator
    quiz_data = generate_quiz_from_text(title, text)
    quiz_data.update(extras)
    quiz_data["url"] = req.url

    # Save quiz to history with an ID
    quiz_record = {
        "id": quiz_id_counter,
        "title": quiz_data.get("title", "No Title"),
        "url": req.url,
        "quiz": quiz_data.get("quiz", []),
        "summary": quiz_data.get("summary", "")
    }
    quiz_history.append(quiz_record)
    quiz_id_counter += 1

    return quiz_record

# -------------------- History Endpoints --------------------
@app.get("/history")
def get_history():
    """Return list of all previously generated quizzes."""
    return quiz_history

@app.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: int):
    """Return quiz details by ID."""
    for q in quiz_history:
        if q["id"] == quiz_id:
            return q
    raise HTTPException(404, "Quiz not found")
