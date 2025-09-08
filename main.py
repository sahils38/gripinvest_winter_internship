from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.db.session import SessionLocal
from app.api import auth as auth_router
from app.middleware.logging import request_logger

app = FastAPI(title="Grip Mini Investment API")

@app.middleware("http")
async def _request_logger_mw(request, call_next):
    return await request_logger(request, call_next)

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

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
