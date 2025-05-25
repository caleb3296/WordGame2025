from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gdown
import random
import pandas as pd
from gensim.models import KeyedVectors

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Keeps local testing
        "https://wordgame2025-frontend.onrender.com"  # Allows live frontend access
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Drive File IDs (Replace with your actual IDs)
word2vec_file_id = "1OnmLfyPOLsdYP5OA8AREz1M4byKfzyOB"
csv_file_id = "1kEdmY7geQQHB1a81JDdpTxWyiizSbyt-"

# Paths for downloaded files
word2vec_path = "./GoogleNews-vectors-negative300.bin.gz"
csv_path = "./most_common.csv"

# Download and load Word2Vec model if not already present
gdown.download(f"https://drive.google.com/uc?id={word2vec_file_id}", word2vec_path, quiet=False)
w = KeyedVectors.load_word2vec_format(word2vec_path, binary=True, limit=50000)  # Adjust limit for size

# Download and load CSV file dynamically
gdown.download(f"https://drive.google.com/uc?id={csv_file_id}", csv_path, quiet=False)
df = pd.read_csv(csv_path)

@app.get("/start")
def start_game():
    word_limit = len(df)
    start_word = df["Word"][random.randint(0, word_limit - 1)]
    finish_word = df["Word"][random.randint(0, word_limit - 1)]
    return {"start_word": start_word, "finish_word": finish_word}

@app.get("/similar/{word}")
def get_similar_words(word: str):
    words = w.most_similar(positive=[word], topn=10)
    return {"similar_words": [w[0] for w in words]}

@app.get("/check_win/{word}/{target}")
def check_win(word: str, target: str):
    return {"win": word == target}