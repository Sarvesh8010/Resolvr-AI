from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import SessionLocal
from app.db.models import ChatHistory
from app.core.auth_middleware import get_current_user

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET USER CHAT HISTORY
@router.get("/")
def get_history(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = db.query(ChatHistory).filter(
        ChatHistory.user_email == user["email"]
    ).order_by(
        ChatHistory.created_at.desc()
    ).all()

    return [
        {
            "id": item.id,
            "query": item.query,
            "answer": item.answer,
            "created_at": item.created_at
        }
        for item in history
    ]