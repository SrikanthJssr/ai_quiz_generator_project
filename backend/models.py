# backend/models.py
from pydantic import BaseModel
from typing import List, Optional, Dict

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str
    difficulty: str

class QuizOutput(BaseModel):
    title: str
    summary: Optional[str]
    sections: Optional[List[str]]
    quiz: List[QuizQuestion]