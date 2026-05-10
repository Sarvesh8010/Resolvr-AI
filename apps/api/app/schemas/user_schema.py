from pydantic import BaseModel

class UserResponse(BaseModel):

    id: int

    full_name: str

    email: str

    role: str

    class Config:
        from_attributes = True