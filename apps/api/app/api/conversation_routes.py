from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.auth_middleware import get_current_user

from app.db.connection import SessionLocal
from app.db.models import Conversation, ChatHistory

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE CONVERSATION
@router.post("/")
def create_conversation(
    title: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    conversation = Conversation(
        user_email=user["email"],
        title=title
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return {
        "id": conversation.id,
        "title": conversation.title
    }


# GET USER CONVERSATIONS
@router.get("/")
def get_conversations(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    conversations = db.query(Conversation).filter(
        Conversation.user_email == user["email"]
    ).order_by(
        Conversation.created_at.desc()
    ).all()

    return [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at
        }
        for conv in conversations
    ]


# GET CONVERSATION MESSAGES
@router.get("/{conversation_id}")
def get_conversation_messages(
    conversation_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    messages = db.query(ChatHistory).filter(
        ChatHistory.conversation_id == conversation_id
    ).order_by(
        ChatHistory.created_at.asc()
    ).all()

    return [
        {
            "id": msg.id,
            "query": msg.query,
            "answer": msg.answer,
            "created_at": msg.created_at
        }
        for msg in messages
    ]

# DELETE CONVERSATION
@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # FIND CONVERSATION
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_email == user["email"]
    ).first()

    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # DELETE CHAT HISTORY
    db.query(ChatHistory).filter(
        ChatHistory.conversation_id == conversation_id
    ).delete()

    # DELETE CONVERSATION
    db.delete(conversation)

    db.commit()

    return {
        "message": "Conversation deleted successfully"
    }

# RENAME CONVERSATION
@router.put("/{conversation_id}")
def rename_conversation(
    conversation_id: int,
    title: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_email == user["email"]
    ).first()

    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    conversation.title = title

    db.commit()

    db.refresh(conversation)

    return {
        "message": "Conversation renamed",
        "conversation": {
            "id": conversation.id,
            "title": conversation.title
        }
    }