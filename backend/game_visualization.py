from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
import logging

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# FastAPI Setup
app = FastAPI()
game_routes = APIRouter()

# Load Word2Vec Model & Word List
filtered_word2vec_path = "./filtered_vectors.bin"
csv_path = "./most_common.csv"
w = KeyedVectors.load(filtered_word2vec_path)
df = pd.read_csv(csv_path)

# Store word path history
word_history = []

# Start Game
@game_routes.get("/start")
async def start_game():
    word_limit = len(df)
    start_word = df["Word"][random.randint(0, word_limit - 1)]
    finish_word = df["Word"][random.randint(0, word_limit - 1)]
    
    word_history.clear()  # Reset path for new game
    word_history.append(start_word)
    
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

# Track User Path
@game_routes.post("/select/{word}")
async def select_word(word: str):
    if word in w.key_to_index:
        word_history.append(word)
        return JSONResponse(content={"path": word_history})
    
    return JSONResponse(content={"error": "Word not found in model"}, status_code=404)

# Generate Word2Vec Visualization
@game_routes.get("/visualize")
async def visualize_path():
    if len(word_history) < 2:
        return JSONResponse(content={"error": "Not enough words selected to visualize a path"}, status_code=400)
    
    # Convert word list to vectors
    vectors = [w[word] for word in word_history if word in w.key_to_index]

    # Reduce Dimensions using PCA
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(np.array(vectors))

    # Extract X, Y coordinates
    x_coords, y_coords = zip(*reduced_vectors)

    # Plot Visualization
    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, color="blue")
    plt.plot(x_coords, y_coords, linestyle="dashed", color="red")

    # Annotate Words
    for i, word in enumerate(word_history):
        plt.text(x_coords[i], y_coords[i], word, fontsize=12, color="green" if i == 0 else "orange")

    plt.title("Word Path in Semantic Space")
    plt.xlabel("X-Dimension")
    plt.ylabel("Y-Dimension")
    plt.savefig("word_path.png")  # Save image
    plt.close()
    
    return JSONResponse(content={"image_path": "word_path.png", "word_history": word_history})

# Include Routes
app.include_router(game_routes)