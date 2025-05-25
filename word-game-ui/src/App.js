import "./App.css";
import React, { useState, useEffect } from "react";
import axios from "axios";

// Dynamically set API base URL
const API_BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8000"
    : "https://wordgame2025.onrender.com";

function App() {
  const [startWord, setStartWord] = useState("");
  const [finishWord, setFinishWord] = useState("");
  const [words, setWords] = useState([]);

  useEffect(() => {
    axios.get(`${API_BASE_URL}/start`, { withCredentials: true })
      .then((response) => {
        setStartWord(response.data.start_word);
        setFinishWord(response.data.finish_word);
        fetchSimilarWords(response.data.start_word);
      })
      .catch((error) => {
        console.error("Error fetching start words:", error);
      });
  }, []);

  const fetchSimilarWords = (word) => {
    axios.get(`${API_BASE_URL}/similar/${word}`, { withCredentials: true })
      .then((response) => {
        setWords(response.data.similar_words);
      })
      .catch((error) => {
        console.error("Error fetching similar words:", error);
      });
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1>Word Game</h1>
      <h2>
        Get from <strong>{startWord}</strong> to <strong>{finishWord}</strong>
      </h2>
      <div>
        {words.map((word) => (
          <button key={word} onClick={() => fetchSimilarWords(word)}>
            {word}
          </button>
        ))}
      </div>
    </div>
  );
}

export default App;