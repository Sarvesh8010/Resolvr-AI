import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


def generate_embeddings(chunks):
    try:
        if not HF_TOKEN:
            raise Exception("HF_TOKEN not set in environment")

        # 🔹 Batch request (efficient)
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": chunks}
        )

        if response.status_code != 200:
            raise Exception(response.text)

        embeddings = response.json()

        # 🔹 Normalize output (HF sometimes nests results)
        normalized_embeddings = []
        for emb in embeddings:
            if isinstance(emb[0], list):
                normalized_embeddings.append(emb[0])
            else:
                normalized_embeddings.append(emb)

        return normalized_embeddings

    except Exception as e:
        raise Exception(f"HF embedding failed: {str(e)}")