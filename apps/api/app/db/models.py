from sqlalchemy import Column, Integer, String, Text, DateTime
from .connection import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    full_name = Column(String, nullable=False)
    
    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )
    
    hashed_password = Column(
        String,
        nullable=False
    )
    
    role = Column(
        String,
        default="employee"
    )

    is_verified = Column(
        Integer,
        default=0
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_by = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    user_email = Column(String, nullable=False)
    
    conversation_id = Column(Integer, nullable=True)

    query = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    user_email = Column(String, nullable=False)

    title = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        nullable=False
    )

    token = Column(
        String,
        unique=True,
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    used = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        nullable=False
    )

    token = Column(
        String,
        unique=True,
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    used = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )