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
  const [movesLeft, setMovesLeft] = useState(100); // Counter for moves
  const [gameOverMessage, setGameOverMessage] = useState(""); // Message for popup

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
    if (movesLeft > 0) {
      setMovesLeft(prev => prev - 1);

      if (word === finishWord) {
        setGameOverMessage("Congratulations! You won! 🎉");
      }
    }

    axios.get(`${API_BASE_URL}/similar/${word}`, { withCredentials: true })
      .then((response) => {
        setWords(response.data.similar_words);
      })
      .catch((error) => {
        console.error("Error fetching similar words:", error);
      });

    if (movesLeft <= 1) {
      setGameOverMessage("Time's up! You lost! 😢");
    }
  };

  const getColor = () => {
    if (movesLeft > 30) return "green";
    if (movesLeft > 10) return "orange"; // Change yellow to orange
    return "red";
  };

  return (
    <div style={{ textAlign: "center", position: "relative" }}>
      <h1>Word Game</h1>
      <h2>
        Get from <strong>{startWord}</strong> to <strong>{finishWord}</strong>
      </h2>

      {/* Move Counter Display */}
      <div
        style={{
          position: "absolute",
          top: "10px",
          right: "10px",
          fontSize: "24px",
          fontWeight: "bold",
          color: getColor(),
        }}
      >
        {movesLeft}
      </div>

      <div>
        {words.map((word) => (
          <button key={word} onClick={() => fetchSimilarWords(word)}>
            {word}
          </button>
        ))}
      </div>

      {/* Game Over Popup */}
      {gameOverMessage && (
        <div className="popup">
          <div className="popup-content">
            <h2>{gameOverMessage}</h2>
            <button onClick={() => window.location.reload()}>Restart Game</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;