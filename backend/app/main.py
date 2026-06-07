from fastapi import FastAPI
from app.db.database import create_tables

app = FastAPI(
    title="Marvel Rivals Optimizer",
    description="Pick/ban optimizer based on meta, counters, synergies, and personal stats",
    version="0.1.0",
)

@app.on_event("startup")
def startup():
    """Run when the app starts and create tables if they don't exist."""
    create_tables()

@app.get("/health")
def health_check():
    """Simple endpoint to verify the API is running"""
    return {"status": "ok"}