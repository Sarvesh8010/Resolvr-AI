from fastapi import FastAPI, Depends
from dotenv import load_dotenv

# Load environment variables (HF, GROQ, etc.)
load_dotenv()

from app.db.connection import Base, engine
from app.api.auth_routes import router as auth_router
from app.api.ingestion_routes import router as ingestion_router
from app.api.query_routes import router as query_router

from app.core.auth_middleware import get_current_user
from app.core.role_checker import require_role

# Ensure models are registered
from app.db import models


app = FastAPI(
    title="Resolvr AI",
    description="Agentic AI Knowledge & Decision Engine",
    version="1.0.0"
)

# Create tables at startup
Base.metadata.create_all(bind=engine)


# ---------------- ROUTERS ----------------
app.include_router(auth_router)
app.include_router(ingestion_router)
app.include_router(query_router)


# ---------------- HEALTH ----------------
@app.get("/")
def root():
    return {"message": "Resolvr AI backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------- AUTH TEST ----------------
@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user": user
    }


# ---------------- ROLE TEST ----------------
@app.get("/admin-only")
def admin_only(user=Depends(require_role("admin"))):
    return {
        "message": "Welcome Admin",
        "user": user
    }