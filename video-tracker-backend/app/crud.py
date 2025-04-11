# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas, utils

def save_progress(db: Session, data: schemas.ProgressCreate):
    record = db.query(models.Progress).filter_by(
        user_id=data.user_id,
        video_id=data.video_id
    ).first()

    new_intervals = data.watched_intervals

    if record:
        combined = record.watched_intervals + new_intervals
        record.watched_intervals = utils.merge_intervals(combined)
        record.last_watched = max(record.last_watched, data.last_watched)
    else:
        merged_intervals = utils.merge_intervals(new_intervals)
        record = models.Progress(
            user_id=data.user_id,
            video_id=data.video_id,
            watched_intervals=merged_intervals,
            last_watched=data.last_watched
        )
        db.add(record)

    db.commit()
    db.refresh(record)
    return record

def get_progress(db: Session, user_id: str, video_id: str):
    return db.query(models.Progress).filter_by(user_id=user_id, video_id=video_id).first()
