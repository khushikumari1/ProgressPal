from pydantic import BaseModel, Field
from typing import List

class ProgressCreate(BaseModel):
    user_id: str = Field(..., min_length=1)
    video_id: str = Field(..., min_length=1)
    watched_intervals: List[List[float]] = Field(default_factory=list)
    last_watched: float = 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "video_id": "video_456",
                "watched_intervals": [[0, 10], [20, 30]],
                "last_watched": 30.0
            }
        }

class ProgressOut(ProgressCreate):
    id: int

    class Config:
        from_attributes = True
