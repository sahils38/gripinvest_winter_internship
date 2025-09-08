from __future__ import annotations
import uuid
from typing import cast, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.models import User as ORMUser
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.schemas.auth import SignupIn, LoginIn, TokenOut
from app.schemas.user import UserOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/signup", status_code=201)
def signup(body: SignupIn, db: Session = Depends(get_db)):
    if db.query(ORMUser).filter(ORMUser.email == str(body.email)).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = ORMUser(
        id=str(uuid.uuid4()),
        first_name=body.first_name,
        last_name=body.last_name,
        email=str(body.email),
        password_hash=hash_password(body.password),
    )
    db.add(user); db.commit()
    return {"id": user.id, "email": user.email}

@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    email_str = str(body.email)
    user = db.query(ORMUser).filter(ORMUser.email == email_str).first()
    if not user or not verify_password(body.password, cast(str, user.password_hash)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=email_str)
    return TokenOut(access_token=token)

def get_current_user(request: Request, db: Session = Depends(get_db)) -> ORMUser:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    email = decode_token(auth.removeprefix("Bearer ").strip())
    if not email:
        raise HTTPException(status_code=401, detail="Invalid/expired token")

    user: ORMUser | None = db.query(ORMUser).filter(ORMUser.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

#Tell the checker this param is “an ORMUser provided by Depends(get_current_user)”
CurrentUser = Annotated[ORMUser, Depends(get_current_user)]

@router.get("/me", response_model=UserOut)
def me(current_user: CurrentUser):
    return UserOut.model_validate(current_user)