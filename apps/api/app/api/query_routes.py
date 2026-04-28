from fastapi import APIRouter, Depends
from app.core.auth_middleware import get_current_user
from app.rag.retriever import retrieve_chunks
from app.agents.answer_generator import generate_answer

router = APIRouter(prefix="/query", tags=["Query"])


@router.get("/")
def query(q: str, user=Depends(get_current_user)):
    chunks = retrieve_chunks(q)
    result = generate_answer(q, chunks)

    return {
        "query": q,
        "answer": result["answer"],
        "sources": result["sources"]
    }