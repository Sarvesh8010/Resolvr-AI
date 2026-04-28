import json
import os

VECTOR_DB_PATH = "vector_store.json"

def store_embeddings(document_id, chunks, embeddings):
    data = []

    if os.path.exists(VECTOR_DB_PATH):
        with open(VECTOR_DB_PATH, "r") as f:
            data = json.load(f)

    for chunk, embedding in zip(chunks, embeddings):
        data.append({
            "document_id": document_id,
            "text": chunk,
            "embedding": embedding
        })

    with open(VECTOR_DB_PATH, "w") as f:
        json.dump(data, f)