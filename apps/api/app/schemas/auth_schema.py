from pydantic import BaseModel

class UserCreate(BaseModel):

    full_name: str

    email: str

    password: str

    role: str = "employee"

class UserLogin(BaseModel):
    email: str
    password: str