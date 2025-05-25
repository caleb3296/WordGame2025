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

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "HEAD", "POST", "*"],  # Wildcard method allowance
    allow_headers=["*"],
)

# Middleware for logging requests and responses
@app.middleware("http")
async def log_request(request: Request, call_next):
    logger.debug(f"Received {request.method} request for {request.url}")
    response = await call_next(request)
    logger.debug(f"Response Status: {response.status_code}, Headers: {response.headers}")
    return response

# Paths for optimized files
filtered_word2vec_path = "./filtered_vectors.bin"
csv_path = "./most_common.csv"

# Load Word2Vec model
w = KeyedVectors.load(filtered_word2vec_path)

# Load CSV file (Word list)
df = pd.read_csv(csv_path)

# Explicitly allow HEAD and GET using api_route
@app.api_route("/start", methods=["GET", "HEAD"])
async def start_game(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content={}, status_code=200)  # Respond to HEAD without body
    
    word_limit = len(df)
    start_word = df["Word"][random.randint(0, word_limit - 1)]
    finish_word = df["Word"][random.randint(0, word_limit - 1)]

    response = JSONResponse(content={"start_word": start_word, "finish_word": finish_word})
    response.headers["Access-Control-Allow-Origin"] = "https://wordgame2025-frontend.onrender.com"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, HEAD"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    return response

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