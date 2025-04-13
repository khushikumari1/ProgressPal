from pydantic import BaseModel, EmailStr, Field, constr
from typing import List, Optional

# 🔐 User-related Schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str
    email: EmailStr

    class Config:
        from_attributes = True

class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class UserResetPassword(BaseModel):
    email: EmailStr
    new_password: constr(min_length=6)

# 📹 Video Progress Schemas

class ProgressCreate(BaseModel):
    user_id: Optional[str] = None  # Filled automatically in protected routes
    video_id: str = Field(..., min_length=1)
    watched_intervals: List[List[float]] = Field(default_factory=list)
    last_watched: float = 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "video_id": "video_456",
                "watched_intervals": [[0, 10], [20, 30]],
                "last_watched": 30.0
            }
        }

class ProgressOut(ProgressCreate):
    id: int

    class Config:
        from_attributes = True
