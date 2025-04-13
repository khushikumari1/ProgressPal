from sqlalchemy.orm import Session
from . import models, schemas
from .utils import merge_intervals
from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)  # Hash the password
    try:
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()  # Commit the transaction
        db.refresh(db_user)  # Refresh the instance with data from the DB
        return db_user
    except Exception as e:
        logging.error(f"Error in creating user: {e}")
        db.rollback()  # Rollback the transaction in case of error
        raise HTTPException(status_code=500, detail="User creation failed")


def save_progress(db: Session, data: schemas.ProgressCreate) -> models.Progress:
    """
    Save or update video progress.
    - Filters out invalid/short intervals.
    - Merges new with existing intervals.
    - Updates last watched timestamp.
    """
    logging.info(f"Saving progress for user {data.user_id}, video {data.video_id}")
    logging.debug(f"Incoming intervals: {data.watched_intervals}")

    # Filter out invalid intervals
    new_intervals = [i for i in data.watched_intervals if i[1] > i[0] and (i[1] - i[0]) >= 1.0]
    if not new_intervals:
        raise ValueError("No valid intervals to save")

    # Fetch existing record
    record = db.query(models.Progress).filter_by(
        user_id=data.user_id,
        video_id=data.video_id
    ).first()

    if record:
        logging.debug(f"Existing intervals: {record.watched_intervals}")
        combined = record.watched_intervals + new_intervals
        record.watched_intervals = merge_intervals(combined)
        record.last_watched = max(record.last_watched or 0.0, data.last_watched or 0.0)
        logging.debug(f"Merged intervals: {record.watched_intervals}")
        db.commit()
        db.refresh(record)
        return record

    else:
        merged = merge_intervals(new_intervals)
        new_record = models.Progress(
            user_id=data.user_id,
            video_id=data.video_id,
            watched_intervals=merged,
            last_watched=data.last_watched
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        logging.debug(f"New progress created: {new_record}")
        return new_record

def get_progress(db: Session, user_id: str, video_id: str) -> models.Progress:
    """
    Fetch progress for a specific user and video.
    If no progress exists, create and return a new record.
    """
    progress = db.query(models.Progress).filter_by(user_id=user_id, video_id=video_id).first()
    if not progress:
        # Create a default progress record if not found
        progress = models.Progress(user_id=user_id, video_id=video_id, watched_intervals=[], last_watched=0.0)
        db.add(progress)
        db.commit()
        db.refresh(progress)
        logging.debug(f"Created new progress record: {progress.watched_intervals}")

    logging.debug(f"Fetched progress: {progress.watched_intervals}")
    return progress


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()