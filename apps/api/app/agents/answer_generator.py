def generate_answer(query: str, chunks: list):
    if not chunks:
        return {
            "answer": "No relevant information found in documents.",
            "sources": []
        }

    context = "\n\n".join([c["text"] for c in chunks])

    # Simple synthesis (no external LLM yet)
    answer = f"Based on the documents:\n\n{context[:1000]}"

    sources = [
        {
            "document_id": c["document_id"],
            "score": c["score"]
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources
    }