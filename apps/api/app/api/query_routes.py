from fastapi import APIRouter, Depends
from app.core.auth_middleware import get_current_user

from app.rag.retriever import retrieve_relevant_chunks
from app.services.llm_service import generate_answer

router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.get("/")
def query_documents(
    q: str,
    user=Depends(get_current_user)
):
    try:
        # --- RETRIEVE RELEVANT CHUNKS ---
        retrieved_chunks = retrieve_relevant_chunks(q)

        # --- BUILD CONTEXT ---
        context = "\n\n".join(
            [chunk["text"] for chunk in retrieved_chunks]
        )

        # --- GENERATE AI ANSWER ---
        answer = generate_answer(q, context)

        # --- EXTRACT SOURCES ---
        sources = list(
            set(
                chunk["source"]
                for chunk in retrieved_chunks
            )
        )

        return {
            "query": q,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        return {
            "error": str(e)
        }