from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.db.session import SessionLocal

app = FastAPI(title="Grip Mini Investment API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health(db = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"service": "ok", "db": "ok"}
