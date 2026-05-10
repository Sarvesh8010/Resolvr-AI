from sentence_transformers import CrossEncoder

from app.rag.vector_store import vector_store


# LOAD RERANKER MODEL
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# ---------------- KEYWORD OVERLAP ----------------

def keyword_overlap_score(
    query: str,
    text: str
):

    query_words = set(
        query.lower().split()
    )

    text_words = set(
        text.lower().split()
    )

    overlap = query_words.intersection(
        text_words
    )

    return len(overlap)


# ---------------- RETRIEVAL ----------------

def retrieve_relevant_chunks(
    query,
    user_email,
    user_role,
    k=5
):

    # VECTOR SEARCH
    # ---------------- ACCESS FILTER ----------------
    
    if user_role == "admin":
    
        results = (
            vector_store
            .similarity_search_with_score(
                query,
                k=10
            )
        )
    
    else:
    
        results = (
            vector_store
            .similarity_search_with_score(
            
                query,
    
                k=10,
    
                filter={
                
                    "$or": [
                    
                        {
                            "uploaded_role":
                            "admin"
                        },
    
                        {
                            "uploaded_by":
                            user_email
                        }
                    ]
                }
            )
        )

    retrieved_chunks = []

    for doc, semantic_score in results:

        text = doc.page_content

        keyword_score = keyword_overlap_score(
            query,
            text
        )

        hybrid_score = (
            float(semantic_score)
            - (keyword_score * 0.15)
        )

        retrieved_chunks.append({
            "text": text,
            "score": hybrid_score,
            "semantic_score": float(
                semantic_score
            ),
            "keyword_score": keyword_score,
            "source": doc.metadata.get(
                "source"
            )
        })

    # INITIAL SORT
    retrieved_chunks = sorted(
        retrieved_chunks,
        key=lambda x: x["score"]
    )

    # TAKE TOP CANDIDATES
    candidates = retrieved_chunks[:10]

    # ---------------- CROSS-ENCODER RERANKING ----------------

    rerank_inputs = [
        (query, chunk["text"])
        for chunk in candidates
    ]

    rerank_scores = reranker.predict(
        rerank_inputs
    )

    for idx, score in enumerate(
        rerank_scores
    ):

        candidates[idx][
            "rerank_score"
        ] = float(score)

    # FINAL RERANK
    candidates = sorted(
        candidates,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    # FINAL TOP CHUNKS
    final_chunks = candidates[:k]

    # CONFIDENCE FILTER
    high_confidence_chunks = [
        chunk
        for chunk in final_chunks
        if chunk["rerank_score"] > 0
    ]

    return high_confidence_chunks