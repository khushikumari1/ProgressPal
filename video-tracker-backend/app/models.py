# app/models.py

from sqlalchemy import Column, Integer, String, Float, JSON, UniqueConstraint
from .database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    video_id = Column(String, index=True)
    watched_intervals = Column(JSON, default=[])
    last_watched = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint('user_id', 'video_id', name='user_video_uc'),
    )
