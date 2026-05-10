from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.connection import SessionLocal

from app.db.models import (
    User,
    Document,
    Conversation
)

from app.core.auth_middleware import (
    get_current_user
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ADMIN CHECK
def require_admin(user):

    if user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


# GET ALL USERS
@router.get("/users")
def get_all_users(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    require_admin(current_user)

    users = db.query(User).all()

    return users


# UPDATE USER ROLE
@router.put("/users/{user_id}/role")
def update_user_role(

    user_id: int,

    role: str,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    require_admin(current_user)

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = role

    db.commit()

    return {
        "message":
        "User role updated"
    }


# DELETE USER
@router.delete("/users/{user_id}")
def delete_user(

    user_id: int,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    require_admin(current_user)

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)

    db.commit()

    return {
        "message":
        "User deleted"
    }


@router.get("/analytics")
def get_admin_analytics(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    require_admin(current_user)

    total_users = db.query(User).count()

    verified_users = db.query(User).filter(
        User.is_verified == 1
    ).count()

    admins = db.query(User).filter(
        User.role == "admin"
    ).count()

    employees = db.query(User).filter(
        User.role == "employee"
    ).count()

    documents = db.query(Document).count()

    conversations = db.query(
        Conversation
    ).count()

    return {

        "total_users":
        total_users,

        "verified_users":
        verified_users,

        "admins":
        admins,

        "employees":
        employees,

        "documents":
        documents,

        "conversations":
        conversations
    }


# GET ALL DOCUMENTS
@router.get("/documents")
def get_all_documents(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    require_admin(current_user)

    documents = db.query(Document).all()

    return documents


# DELETE DOCUMENT
@router.delete("/documents/{document_id}")
def delete_document(

    document_id: int,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    require_admin(current_user)

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(document)

    db.commit()

    return {
        "message":
        "Document deleted"
    }