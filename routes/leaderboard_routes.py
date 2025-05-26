from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import get_db, LeaderboardEntry
from pydantic import BaseModel

# Router
leaderboard_routes = APIRouter()

# Leaderboard Entry Schema
class LeaderboardEntryInput(BaseModel):
    player_name: str
    score: int

# Add Score
@leaderboard_routes.post("/leaderboard")
def add_score(entry: LeaderboardEntryInput, db: Session = Depends(get_db)):
    new_entry = LeaderboardEntry(player_name=entry.player_name, score=entry.score)
    db.add(new_entry)
    db.commit()
    return JSONResponse(content={"message": "Score added successfully!"})

# Get Leaderboard
@leaderboard_routes.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """Retrieve leaderboard scores."""
    top_scores = db.query(LeaderboardEntry).order_by(LeaderboardEntry.score.asc()).limit(10).all()
    return JSONResponse(content={"leaderboard": [{"player": entry.player_name, "score": entry.score} for entry in top_scores]})