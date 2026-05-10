from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from app.core.auth_middleware import get_current_user

from app.db.connection import SessionLocal

from app.db.models import (
    ChatHistory,
    Conversation
)

from app.rag.retriever import retrieve_relevant_chunks

from app.services.llm_service import generate_streaming_answer

router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stream")
def stream_query(
    q: str,
    conversation_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # VALIDATE CONVERSATION
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_email == user["email"]
    ).first()

    if not conversation:
        return {
            "error": "Conversation not found"
        }

    # RETRIEVE RELEVANT CHUNKS
    # ---------------- MEMORY-AWARE QUERY ----------------
    
    recent_history = db.query(ChatHistory).filter(
        ChatHistory.conversation_id == conversation_id
    ).order_by(
        ChatHistory.created_at.desc()
    ).limit(3).all()
    
    history_context = ""
    
    for chat in reversed(recent_history):
    
        history_context += (
            f"User: {chat.query}\n"
            f"Assistant: {chat.answer}\n\n"
        )
    
    enhanced_query = (
        history_context +
        f"User: {q}"
    )
    
    # ---------------- RETRIEVAL ----------------
    
    retrieved_chunks = retrieve_relevant_chunks(
        
        enhanced_query,
    
        user_email=user["email"],
    
        user_role=user["role"]
    )

    # NO RELEVANT CONTEXT
    if not retrieved_chunks:
    
        def no_context():
        
            yield (
                "I could not find relevant "
                "information in the uploaded "
                "documents."
            )
    
        return StreamingResponse(
            no_context(),
            media_type="text/plain"
        )

    # BUILD CONTEXT
    context = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    )

    # STORE FULL RESPONSE
    full_answer = ""

    # STREAM GENERATOR
    def generate():

        nonlocal full_answer

        for chunk in generate_streaming_answer(q, context):

            full_answer += chunk

            yield chunk

        # SAVE CHAT
        chat = ChatHistory(
            user_email=user["email"],
            conversation_id=conversation_id,
            query=q,
            answer=full_answer
        )

        db.add(chat)

        db.commit()

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )