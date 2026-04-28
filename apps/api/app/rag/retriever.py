import json
import os
import numpy as np
import requests

VECTOR_DB_PATH = "vector_store.json"

HF_TOKEN = os.getenv("HF_TOKEN")
HF_EMBEDDING_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_query_embedding(query: str):
    response = requests.post(
        HF_EMBEDDING_URL,
        headers=headers,
        json={"inputs": query}
    )

    if response.status_code != 200:
        raise Exception(f"HF embedding failed: {response.text}")

    return response.json()[0]  # flatten


def retrieve_chunks(query: str, top_k: int = 3):
    if not os.path.exists(VECTOR_DB_PATH):
        return []

    # Load stored vectors
    with open(VECTOR_DB_PATH, "r") as f:
        data = json.load(f)

    # Embed query using HF
    query_embedding = get_query_embedding(query)

    scored = []

    for item in data:
        embedding = item["embedding"]

        score = cosine_similarity(query_embedding, embedding)

        scored.append({
            "text": item["text"],
            "score": float(score),
            "document_id": item["document_id"]
        })

    # Sort by similarity
    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:top_k]