import React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Oops! Page Not Found 😕</h2>
      <p>Let's get you back in the game!</p>
      <Link to="/">
        <button>Start New Game</button>
      </Link>
      <Link to="/leaderboard">
        <button>View Leaderboard</button>
      </Link>
    </div>
  );
}

export default NotFound;