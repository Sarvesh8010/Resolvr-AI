from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "employee"

class UserLogin(BaseModel):
    email: str
    password: str