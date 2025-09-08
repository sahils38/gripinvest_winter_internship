from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGO = "HS256"
ACCESS_MIN = 60

def hash_password(plain: str) -> str:
    """Why: Never store plaintext; bcrypt adds salt+work factor."""
    return pwd.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """Why: Constant-time verify; prevents timing leaks."""
    return pwd.verify(plain, hashed)

def create_access_token(sub: str, minutes: int = ACCESS_MIN) -> str:
    """
    Why: Generate a signed token with an expiry.
    sub = 'subject' (who the token represents) — we’ll use the user's email.
    """
    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=minutes)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGO)

def decode_token(token: str) -> Optional[str]:
    """Why: Validate and extract 'sub' (email). Returns None if invalid/expired."""
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms=[ALGO])
        return data.get("sub")
    except jwt.PyJWTError:
        return None
