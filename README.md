# AI Wiki Quiz Generator

A Streamlit-based web application that automatically generates quizzes from Wikipedia articles using **Google Gemini LLM**. This tool is designed for educators, students, and enthusiasts to create structured quizzes effortlessly.

---

## **🔹 Features**

- Generate multiple-choice quizzes automatically from any Wikipedia article.
- Each quiz includes:
  - Questions
  - Multiple-choice options
  - Correct answer
  - Detailed explanations
  - Difficulty levels (easy, medium, hard)
- View **previously generated quizzes** (history tab).
- Clean and interactive UI with tabs for **Quiz Generation** and **History**.
- Supports **long Wikipedia articles** and generates well-structured JSON quizzes.
- Easy to extend with new features, including PDF export, images, and diagrams.

---

## **🔹 Tech Stack**

| Layer         | Technology                        |
|---------------|----------------------------------|
| Frontend      | Streamlit                        |
| Backend       | FastAPI                           |
| AI Model      | Google Gemini (`google.generativeai`) |
| Database      | JSON file (for quiz history)     |
| Language      | Python 3.10+                     |
| Environment   | Virtual Environment (venv)       |

---
