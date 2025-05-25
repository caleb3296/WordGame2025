import "./App.css";
import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8000"
    : "https://wordgame2025.onrender.com";

function App() {
  const [startWord, setStartWord] = useState("");
  const [finishWord, setFinishWord] = useState("");
  const [words, setWords] = useState([]);
  const [testMode, setTestMode] = useState(window.location.pathname === "/test");

  useEffect(() => {
    if (!testMode) {
      axios.get(`${API_BASE_URL}/start`, { withCredentials: true })
        .then((response) => {
          setStartWord(response.data.start_word);
          setFinishWord(response.data.finish_word);
          fetchSimilarWords(response.data.start_word);
        })
        .catch((error) => {
          console.error("Error fetching start words:", error);
        });
    }
  }, [testMode]);

  const fetchSimilarWords = (word) => {
    axios.get(`${API_BASE_URL}/similar/${word}`, { withCredentials: true })
      .then((response) => {
        setWords(response.data.similar_words);
      })
      .catch((error) => {
        console.error("Error fetching similar words:", error);
      });
  };

  const handleTestModeSubmit = () => {
    axios.post(`${API_BASE_URL}/test`, { start_word: startWord, finish_word: finishWord })
      .then((response) => {
        fetchSimilarWords(response.data.start_word);
      })
      .catch((error) => {
        console.error("Error in test mode:", error);
      });
  };

  return (
    <div style={{ textAlign: "center", position: "relative" }}>
      <h1>Word Game {testMode && "(Test Mode)"}</h1>

      {testMode ? (
        <div>
          <h2>Enter your own start and target words:</h2>
          <input type="text" placeholder="Start Word" value={startWord} onChange={e => setStartWord(e.target.value)} />
          <input type="text" placeholder="Target Word" value={finishWord} onChange={e => setFinishWord(e.target.value)} />
          <button onClick={handleTestModeSubmit}>Start Game</button>
        </div>
      ) : (
        <h2>
          Get from <strong>{startWord}</strong> to <strong>{finishWord}</strong>
        </h2>
      )}

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