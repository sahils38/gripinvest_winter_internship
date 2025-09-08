from pydantic import BaseModel, EmailStr, ConfigDict

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    first_name: str
    last_name: str | None = None
    email: EmailStr
    risk_appetite: str
