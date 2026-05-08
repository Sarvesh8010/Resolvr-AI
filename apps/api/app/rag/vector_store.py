from langchain_chroma import Chroma
from app.rag.embedder import embedding_model

VECTOR_DB_PATH = "chroma_db"

vector_store = Chroma(
    collection_name="documents",
    embedding_function=embedding_model,
    persist_directory=VECTOR_DB_PATH
)