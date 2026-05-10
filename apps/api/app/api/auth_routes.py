from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from uuid import uuid4
from datetime import datetime, timedelta

from app.db.models import (
    User,
    PasswordResetToken,
    EmailVerificationToken
)

from app.core.security import (
    hash_password
)

from app.services.email_service import (
    send_verification_email,
    send_password_reset_email
)

from app.db.connection import SessionLocal
from app.schemas.auth_schema import UserCreate
from app.schemas.user_schema import UserResponse
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token
from app.core.auth_middleware import get_current_user

# Create router FIRST
router = APIRouter(prefix="/auth", tags=["Auth"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Signup
@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # CHECK EXISTING EMAIL
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    created_user = create_user(
        db,
        user.full_name,
        user.email,
        user.password,
        user.role
    )

    # GENERATE VERIFICATION TOKEN
    verification_token = str(uuid4())

    expires_at = (
        datetime.utcnow()
        + timedelta(hours=24)
    )

    verification_entry = EmailVerificationToken(

        email=user.email,

        token=verification_token,

        expires_at=expires_at
    )

    db.add(verification_entry)

    db.commit()

    send_verification_email(
        user.email,
        verification_token
    )

    return {
        "id": created_user.id,
        "full_name": created_user.full_name,
        "email": created_user.email,
        "role": created_user.role,
        "message":
        "Verification email sent"
    }


@router.post("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db)
):

    verification_entry = db.query(
        EmailVerificationToken
    ).filter(
        EmailVerificationToken.token == token
    ).first()

    if not verification_entry:

        raise HTTPException(
            status_code=400,
            detail="Invalid verification token"
        )

    if verification_entry.used:

        raise HTTPException(
            status_code=400,
            detail="Token already used"
        )

    if (
        datetime.utcnow()
        >
        verification_entry.expires_at
    ):

        raise HTTPException(
            status_code=400,
            detail="Verification token expired"
        )

    user = db.query(User).filter(
        User.email ==
        verification_entry.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_verified = 1

    verification_entry.used = 1

    db.commit()

    return {
        "message":
        "Email verified successfully"
    }


# Login (OAuth2 compatible)
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not db_user.is_verified:

        raise HTTPException(
            status_code=403,
            detail="Please verify your email before logging in"
        )

    token = create_access_token({
        "sub": db_user.email,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/forgot-password")
def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    # SECURITY:
    # don't reveal whether email exists
    if not user:

        return {
            "message":
            "If the email exists, a reset link has been generated."
        }

    reset_token = str(uuid4())

    expires_at = (
        datetime.utcnow()
        + timedelta(hours=1)
    )

    token_entry = PasswordResetToken(

        email=email,

        token=reset_token,

        expires_at=expires_at
    )

    db.add(token_entry)
    
    db.commit()
    
    send_password_reset_email(
        email,
        reset_token
    )
    
    return {
        "message":
        "Password reset email sent"
    }


@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):

    token_entry = db.query(
        PasswordResetToken
    ).filter(
        PasswordResetToken.token == token
    ).first()

    if not token_entry:

        raise HTTPException(
            status_code=400,
            detail="Invalid token"
        )

    if token_entry.used:

        raise HTTPException(
            status_code=400,
            detail="Token already used"
        )

    if datetime.utcnow() > token_entry.expires_at:

        raise HTTPException(
            status_code=400,
            detail="Token expired"
        )

    user = db.query(User).filter(
        User.email == token_entry.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.hashed_password = hash_password(
        new_password
    )

    token_entry.used = 1

    db.commit()

    return {
        "message":
        "Password reset successful"
    }


@router.get("/me")
def get_me(
    user=Depends(get_current_user)
):

    return {
        "email": user["email"],
        "role": user["role"]
    }