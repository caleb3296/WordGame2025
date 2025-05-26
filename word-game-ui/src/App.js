import "./App.css";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Navbar from "./Navbar";  // ✅ Import Navbar
import NotFound from "./NotFound";  // ✅ Import NotFound

// ✅ Now `Navbar` and `NotFound` are used correctly!

const API_BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8000"
    : "https://wordgame2025.onrender.com";

function App() {
  const [startWord, setStartWord] = useState("");
  const [finishWord, setFinishWord] = useState("");
  const [words, setWords] = useState([]);
  const [testMode, setTestMode] = useState(window.location.pathname === "/test");
  const [gameOverMessage, setGameOverMessage] = useState(""); 
  const [leaderboard, setLeaderboard] = useState([]); // ✅ Store leaderboard data
  const [clickCount, setClickCount] = useState(0); // ✅ Track clicks

  useEffect(() => {
    fetchLeaderboard();
  }, []);

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
    if (word === finishWord) {
      setGameOverMessage("🎉 You won! View the leaderboard! 🎉");
      submitScore(); // ✅ Send score to leaderboard
      return;
    }
  
    setClickCount(clickCount + 1); // ✅ Increment click count
    
    axios.get(`${API_BASE_URL}/similar/${word}`, { withCredentials: true })
      .then((response) => {
        setWords(response.data.similar_words);
      })
      .catch((error) => {
        console.error("Error fetching similar words:", error);
      });
  };

  const fetchLeaderboard = () => {
    axios.get(`${API_BASE_URL}/leaderboard`)
      .then((response) => {
        setLeaderboard(response.data.leaderboard);
      })
      .catch((error) => {
        console.error("Error fetching leaderboard:", error);
      });
  };

  const submitScore = () => {
    axios.post(`${API_BASE_URL}/leaderboard?score=${clickCount}&start_word=${startWord}&finish_word=${finishWord}`)
      .then(() => {
        fetchLeaderboard(); // ✅ Refresh leaderboard after submitting score
      })
      .catch((error) => {
        console.error("Error submitting score:", error);
      });
  };

  return (
    <Router>
      <div style={{ textAlign: "center", position: "relative" }}>
        <h1>Word Game {testMode && "(Test Mode)"}</h1>

        <Routes>
          {/* ✅ Main Game Screen */}
          <Route path="/" element={
            <>
              {testMode ? (
                <div>
                  <h2>Enter your own start and target words:</h2>
                  <input 
                    type="text" 
                    placeholder="Start Word" 
                    value={startWord} 
                    onChange={e => setStartWord(e.target.value)} 
                  />
                  <input 
                    type="text" 
                    placeholder="Target Word" 
                    value={finishWord} 
                    onChange={e => setFinishWord(e.target.value)} 
                  />
                  <button onClick={() => submitScore()}>Start Game</button>
                </div>
              ) : (
                <h2>Get from <strong>{startWord}</strong> to <strong>{finishWord}</strong></h2>
              )}

              <div>
                {words.map((word) => (
                  <button key={word} onClick={() => fetchSimilarWords(word)}>
                    {word}
                  </button>
                ))}
              </div>

              {/* ✅ Game Over Popup with Leaderboard Prompt */}
              {gameOverMessage && (
                <div className="popup">
                  <div className="popup-content">
                    <h2>{gameOverMessage}</h2>
                    <Link to="/leaderboard">
                      <button>View Leaderboard</button>
                    </Link>
                    <button onClick={() => window.location.reload()}>Restart Game</button>
                  </div>
                </div>
              )}
            </>
          } />

          {/* ✅ Leaderboard Page */}
          <Route path="/leaderboard" element={
            <div>
              <h2>Leaderboard</h2>
              <table>
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Clicks (Steps)</th>
                    <th>Start Word</th>
                    <th>Finish Word</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.sort((a, b) => a.score - b.score).map((entry, index) => (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      <td>{entry.score}</td>
                      <td>{entry.start_word}</td>
                      <td>{entry.finish_word}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <Link to="/">
                <button>Back to Game</button>
              </Link>
            </div>
          } />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
