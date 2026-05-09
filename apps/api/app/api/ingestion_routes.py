from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os
from datetime import datetime
from sqlalchemy.orm import Session
from langchain_core.documents import Document as LangchainDocument

from app.ingestion.parser.parser import parse_file
from app.core.role_checker import require_role
from app.db.connection import SessionLocal
from app.db.models import Document

from app.rag.chunker import chunk_text
from app.rag.vector_store import vector_store

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

UPLOAD_DIR = "uploaded_files"
ALLOWED_EXTENSIONS = {"pdf", "csv", "xlsx", "eml"}

os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    try:

        # ---------------- VALIDATION ----------------
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Invalid file"
            )

        extension = file.filename.split(".")[-1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        # ---------------- SAVE FILE ----------------
        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # ---------------- PARSE FILE ----------------
        try:
            parsed_content = parse_file(
                file_path,
                extension
            )

        except Exception as parse_error:
            raise HTTPException(
                status_code=400,
                detail=f"Parsing failed: {str(parse_error)}"
            )

        # ---------------- CHECK EMPTY CONTENT ----------------
        if not parsed_content or not parsed_content.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found inside the uploaded document."
            )

        # ---------------- STORE METADATA ----------------
        doc = Document(
            filename=file.filename,
            file_type=extension,
            file_path=file_path,
            uploaded_by=user["email"],
            uploaded_at=datetime.utcnow()
        )

        db.add(doc)
        db.commit()
        db.refresh(doc)

        # ---------------- CHUNK TEXT ----------------
        chunks = chunk_text(parsed_content)

        # ---------------- CHECK EMPTY CHUNKS ----------------
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Document could not be converted into chunks."
            )

        # ---------------- CREATE LANGCHAIN DOCS ----------------
        documents = [
            LangchainDocument(
                page_content=chunk,
                metadata={
                    "source": file.filename,
                    "document_id": doc.id
                }
            )
            for chunk in chunks
        ]

        # ---------------- CHECK EMPTY DOCUMENTS ----------------
        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No valid embeddings could be created."
            )

        # ---------------- VECTOR STORE ----------------
        try:
            vector_store.add_documents(documents)

        except Exception as rag_error:
            print("RAG ERROR:", rag_error)

            import traceback
            traceback.print_exc()

            raise HTTPException(
                status_code=500,
                detail=f"RAG pipeline failed: {str(rag_error)}"
            )

        # ---------------- RESPONSE ----------------
        return {
            "message": "File uploaded and processed successfully",
            "document_id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "chunks_created": len(chunks),
            "preview": parsed_content[:500]
        }

    except HTTPException as e:
        
        print("HTTP ERROR:", e.detail)
    
        import traceback
        traceback.print_exc()
    
        raise
    
    except Exception as e:
    
        print("GENERAL ERROR:", str(e))
    
        import traceback
        traceback.print_exc()
    
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )