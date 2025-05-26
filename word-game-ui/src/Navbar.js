import React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="navbar">
      <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>☰</button>
      {menuOpen && (
        <div className="menu">
          <Link to="/">New Game</Link>
          <Link to="/leaderboard">Leaderboard</Link>
        </div>
      )}
    </div>
  );
}

export default Navbar;