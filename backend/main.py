from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import traceback

from scraper import extract_text_from_wiki
from llm_quiz_generator import generate_quiz_from_text

app = FastAPI(title="AI Quiz Generator")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Models --------------------
class QuizRequest(BaseModel):
    url: str

# -------------------- In-Memory History --------------------
quiz_history = []
quiz_id_counter = 1

# -------------------- Endpoints --------------------
@app.get("/")
def home():
    return {"status": "✅ Backend is running"}

@app.get("/extract")
def extract(url: str):
    try:
        title, text, extras = extract_text_from_wiki(url)
        if not text:
            raise HTTPException(400, "Could not extract article text.")
        return {"title": title, "text": text, "extras": extras}
    except Exception as e:
        print(f"Error in /extract: {e}")
        traceback.print_exc()
        raise HTTPException(500, f"Internal server error: {e}")

@app.post("/generate_quiz")
def generate(req: QuizRequest):
    global quiz_id_counter
    try:
        title, text, extras = extract_text_from_wiki(req.url)
        if not text:
            raise HTTPException(400, "Could not extract text from article.")

        quiz_data = generate_quiz_from_text(title, text)
        quiz_data.update(extras)
        quiz_data["url"] = req.url

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
    except Exception as e:
        # Log full traceback in Render logs
        print(f"Error in /generate_quiz: {e}")
        traceback.print_exc()
        raise HTTPException(500, f"Internal server error: {e}")

@app.get("/history")
def get_history():
    return quiz_history

@app.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: int):
    for q in quiz_history:
        if q["id"] == quiz_id:
            return q
    raise HTTPException(404, "Quiz not found")

# -------------------- Deployment Entry --------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Cloud platforms usually provide PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
