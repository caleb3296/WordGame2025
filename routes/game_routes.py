from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import random
import pandas as pd
from gensim.models import KeyedVectors
import logging

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Router
game_routes = APIRouter()

# Load data
filtered_word2vec_path = "./filtered_vectors.bin"
csv_path = "./most_common.csv"
w = KeyedVectors.load(filtered_word2vec_path)
df = pd.read_csv(csv_path)

# Start Game
@game_routes.get("/start")
async def start_game():
    word_limit = len(df)
    start_word = df["Word"][random.randint(0, word_limit - 1)]
    finish_word = df["Word"][random.randint(0, word_limit - 1)]
    return JSONResponse(content={"start_word": start_word, "finish_word": finish_word})

# Fetch Similar Words
@game_routes.get("/similar/{word}")
async def get_similar_words(word: str):
    logger.debug(f"Fetching similar words for: {word}")
    if word in w.key_to_index:
        words = w.most_similar(positive=[word], topn=10)
        return JSONResponse(content={"similar_words": [w[0] for w in words]})
    
    logger.warning(f"No similar words found for '{word}'")
    return JSONResponse(content={"error": f"No similar words found for '{word}'"}, status_code=404)