from pydantic import BaseModel, EmailStr

class SignupIn(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
