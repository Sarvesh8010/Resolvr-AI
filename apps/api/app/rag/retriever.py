from app.rag.vector_store import vector_store

def retrieve_relevant_chunks(query, k=3):
    results = vector_store.similarity_search_with_score(query, k=k)

    retrieved_chunks = []

    for doc, score in results:
        retrieved_chunks.append({
            "text": doc.page_content,
            "score": score,
            "source": doc.metadata.get("source")
        })

    return retrieved_chunks