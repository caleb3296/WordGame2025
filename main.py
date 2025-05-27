from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.game_routes import game_routes  # ✅ Correct import
from routes.leaderboard_routes import leaderboard_routes  # ✅ Correct import
from backend.game_visualization import game_routes  # ✅ Explicit backend module path


app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://wordgame2025-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "HEAD"],
    allow_headers=["*"],
)

# Register routes
app.include_router(game_routes)
app.include_router(leaderboard_routes)

# ✅ Base Route (Health Check)
@app.get("/")
async def root():
    return {"message": "Word Game API is running!"}