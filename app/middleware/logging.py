from __future__ import annotations
from typing import Optional
from fastapi import Request
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import TransactionLog
from app.core.security import decode_token

async def request_logger(request: Request, call_next):
    raw_auth = request.headers.get("Authorization", "")
    email: Optional[str] = None
    if raw_auth.startswith("Bearer "):
        email = decode_token(raw_auth.removeprefix("Bearer ").strip())

    endpoint = request.url.path
    method = request.method
    status_code = 500
    error_message: Optional[str] = None

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception as exc:
        error_message = str(exc)
        raise
    finally:
        db: Session = SessionLocal()
        try:
            db.add(TransactionLog(
                user_id=None,
                email=email,
                endpoint=endpoint,
                http_method=method,
                status_code=status_code,
                error_message=error_message,
            ))
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()
