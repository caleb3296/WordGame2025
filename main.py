from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random
import pandas as pd
from gensim.models import KeyedVectors

app = FastAPI()

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Allows local development
        "https://wordgame2025-frontend.onrender.com"  # Allows live frontend access
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Paths for optimized files
filtered_word2vec_path = "./filtered_vectors.bin"
csv_path = "./most_common.csv"

# Load the smaller Word2Vec model (MUCH faster now!)
w = KeyedVectors.load(filtered_word2vec_path)

# Load CSV file (Word list)
df = pd.read_csv(csv_path)

@app.get("/start")
def start_game():
    word_limit = len(df)
    start_word = df["Word"][random.randint(0, word_limit - 1)]
    finish_word = df["Word"][random.randint(0, word_limit - 1)]

    response = JSONResponse(content={"start_word": start_word, "finish_word": finish_word})
    response.headers["Access-Control-Allow-Origin"] = "https://wordgame2025-frontend.onrender.com"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    return response

@app.get("/similar/{word}")
def get_similar_words(word: str):
    """Fetch similar words using Word2Vec."""
    if word in w.key_to_index:
        words = w.most_similar(positive=[word], topn=10)
        return {"similar_words": [w[0] for w in words]}
    else:
        return JSONResponse(content={"error": "Word not found in model"}, status_code=404)

@app.get("/check_win/{word}/{target}")
def check_win(word: str, target: str):
    """Check if the user has reached the target word."""
    return {"win": word == target}