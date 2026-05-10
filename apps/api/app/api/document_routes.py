from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.core.role_checker import require_role

from sqlalchemy.orm import Session

from app.db.connection import SessionLocal

from app.db.models import (
    Document,
    User
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
    prefix="/documents",
    tags=["Documents"]
)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET ALL DOCUMENTS
@router.get("/")
def get_documents(
    user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    documents = db.query(Document).all()

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "uploaded_by": doc.uploaded_by,
            "uploaded_at": doc.uploaded_at
        }
        for doc in documents
    ]


# DELETE DOCUMENT
@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # DELETE FILE FROM STORAGE
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    # DELETE FROM DATABASE
    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }


# GET CURRENT USER DOCUMENTS
@router.get("/my-documents")
def get_my_documents(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    documents = db.query(Document).filter(
        Document.uploaded_by ==
        current_user.email
    ).all()

    return documents


# DELETE OWN DOCUMENT
@router.delete("/my-documents/{document_id}")
def delete_my_document(

    document_id: int,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # OWNERSHIP CHECK
    if (
        document.uploaded_by
        != current_user.email
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(document)

    db.commit()

    return {
        "message":
        "Document deleted"
    }