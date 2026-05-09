from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os

from app.db.connection import SessionLocal
from app.db.models import Document
from app.core.role_checker import require_role

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