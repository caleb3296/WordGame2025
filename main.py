from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random
import pandas as pd
from gensim.models import KeyedVectors

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"  # Allow local testing
        #"https://wordgame2025-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "HEAD"],
    allow_headers=["*"],  # Allow all headers
)


@app.middleware("http")
async def handle_options_request(request: Request, call_next):
    allowed_origins = [
        "http://localhost:3000",
        "https://wordgame2025-frontend.onrender.com"
    ]
    
    origin = request.headers.get("Origin")
    if request.method == "OPTIONS" and origin in allowed_origins:
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, HEAD",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
        return JSONResponse(content={}, headers=headers, status_code=200)

    response = await call_next(request)
    return response


# Paths for optimized files
filtered_word2vec_path = "./filtered_vectors.bin"
csv_path = "./most_common.csv"

# Load Word2Vec model
w = KeyedVectors.load(filtered_word2vec_path)

# Load CSV file (Word list)
df = pd.read_csv(csv_path)

@app.api_route("/start", methods=["GET", "HEAD", "OPTIONS"])
async def start_game(request: Request):
    headers = {
        "Access-Control-Allow-Origin": "https://wordgame2025-frontend.onrender.com",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS, HEAD",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }

    # Handle OPTIONS requests for CORS preflight
    if request.method == "OPTIONS":
        return JSONResponse(content={}, headers=headers, status_code=200)

    # Handle HEAD requests
    if request.method == "HEAD":
        return JSONResponse(content={}, headers=headers, status_code=200)

    word_limit = len(df)
    start_word = df["Word"][random.randint(0, word_limit - 1)]
    finish_word = df["Word"][random.randint(0, word_limit - 1)]

    return JSONResponse(content={"start_word": start_word, "finish_word": finish_word}, headers=headers)

@app.head("/similar/{word}")
@app.get("/similar/{word}")
async def get_similar_words(word: str):
    """Fetch similar words using Word2Vec."""
    if word in w.key_to_index:
        words = w.most_similar(positive=[word], topn=10)
        return JSONResponse(content={"similar_words": [w[0] for w in words]})
    
    # Handle HEAD requests gracefully
    return JSONResponse(content={}, status_code=200)

@app.head("/check_win/{word}/{target}")
@app.get("/check_win/{word}/{target}")
async def check_win(word: str, target: str):
    """Check if the user has reached the target word."""
    
    # Handle HEAD requests gracefully
    if request.method == "HEAD":
        return JSONResponse(content={}, status_code=200)
    
    return JSONResponse(content={"win": word == target})

### **New Test Mode Endpoint**
@app.post("/test")
async def test_mode(data: dict):
    """Accepts user-defined start and finish words."""
    start_word = data.get("start_word")
    finish_word = data.get("finish_word")

    if not start_word or not finish_word:
        return JSONResponse(content={"error": "Both words are required!"}, status_code=400)

    return JSONResponse(content={"start_word": start_word, "finish_word": finish_word})