from sqlalchemy.orm import Session
from app.db import models
from app.core.security import hash_password, verify_password

def create_user(db: Session, email: str, password: str, role: str):
    user = models.User(
        email=email,
        hashed_password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user