import React, { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [quiz, setQuiz] = useState([]);
  const [title, setTitle] = useState("");
  const [score, setScore] = useState(null);
  const [answers, setAnswers] = useState({});

  const generateQuiz = async () => {
    setScore(null);

    const response = await fetch("http://127.0.0.1:8000/generate_quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();
    setTitle(data.title || "Generated Quiz");
    setQuiz(data.quiz || []);
  };

  const selectAnswer = (qIndex, option) => {
    setAnswers({ ...answers, [qIndex]: option });
  };

  const submitQuiz = () => {
    let sc = 0;
    quiz.forEach((q, i) => {
      if (answers[i] === q.answer) sc++;
    });
    setScore(sc);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Wikipedia Quiz Generator</h1>

      <div style={styles.inputBox}>
        <input
          type="text"
          placeholder="Paste Wikipedia URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={styles.input}
        />
        <button onClick={generateQuiz} style={styles.button}>
          Generate Quiz
        </button>
      </div>

      {title && <h2 style={styles.title}>{title}</h2>}

      {quiz.map((q, index) => (
        <div key={index} style={styles.card}>
          <p style={styles.question}>
            {index + 1}. {q.question}
          </p>

          {q.options.map((opt, i) => (
            <label key={i} style={styles.optionLabel}>
              <input
                type="radio"
                name={`q-${index}`}
                value={opt}
                onChange={() => selectAnswer(index, opt)}
              />
              {opt}
            </label>
          ))}
        </div>
      ))}

      {quiz.length > 0 && (
        <button onClick={submitQuiz} style={styles.submitBtn}>
          Submit Quiz
        </button>
      )}

      {score !== null && (
        <h2 style={styles.score}>
          ✅ Your Score: {score} / {quiz.length}
        </h2>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "800px",
    margin: "auto",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
  heading: {
    textAlign: "center",
  },
  inputBox: {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
  },
  input: {
    flex: 1,
    padding: "10px",
    fontSize: "16px",
  },
  button: {
    padding: "10px 14px",
    fontSize: "16px",
    cursor: "pointer",
    backgroundColor: "#0077ff",
    color: "white",
    border: "none",
    borderRadius: "5px",
  },
  title: {
    marginTop: "10px",
    marginBottom: "15px",
    fontWeight: "bold",
    fontSize: "20px",
  },
  card: {
    background: "#f8f8f8",
    padding: "15px",
    borderRadius: "8px",
    marginBottom: "15px",
    border: "1px solid #ddd",
  },
  question: {
    fontWeight: "bold",
    marginBottom: "10px",
  },
  optionLabel: {
    display: "block",
    marginBottom: "6px",
    cursor: "pointer",
  },
  submitBtn: {
    padding: "12px 20px",
    backgroundColor: "green",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "16px",
    cursor: "pointer",
    display: "block",
    margin: "auto",
    marginTop: "20px",
  },
  score: {
    textAlign: "center",
    marginTop: "20px",
    fontSize: "24px",
    fontWeight: "bold",
  },
};

export default App;
