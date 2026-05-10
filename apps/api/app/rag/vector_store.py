from langchain_chroma import Chroma
from app.rag.embedder import embedding_model

CHROMA_DB_DIR = "chroma_db"

vector_store = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embedding_model
)


# ---------------- DELETE DOCUMENT VECTORS ----------------

def delete_document_vectors(document_id: int):

    collection = vector_store._collection

    results = collection.get(
        where={
            "document_id": document_id
        }
    )

    ids = results.get("ids", [])

    if ids:
        collection.delete(ids=ids)