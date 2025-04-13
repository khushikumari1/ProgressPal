from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from . import crud, schemas, auth, models
from .dependencies import get_db, get_current_user
from .utils import merge_intervals  
from dotenv import load_dotenv
import os
import logging
from app import crud


# Load environment variables from .env
load_dotenv()

# Config vars
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Initialize app
app = FastAPI(title="ProgressPal - Video Tracker")

# CORS for frontend (adjust frontend domain if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)


try:
    # Try to connect to the database
    engine.connect()
    print("Database connection successful!")
except OperationalError as e:
    print("Error connecting to the database:", e)

# Setup logging
logging.basicConfig(level=logging.INFO)

# ======= USER ROUTES =======

@app.post("/signup", status_code=201)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        # Log the incoming data
        logging.info(f"Attempting to create a new user with email: {user.email}")
        new_user = crud.create_user(db, user)
        logging.info(f"User created successfully: {new_user.email}")
        return new_user
    except Exception as e:
        # Log the full exception for debugging
        logging.error(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Signup failed. Please try again later.")

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

# ======= PROGRESS ROUTES =======

@app.post("/progress", response_model=schemas.ProgressOut)
def save_progress(
    data: schemas.ProgressCreate,
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(get_current_user) 
):
    logging.info(f"Saving progress for user {data.user_id}, video {data.video_id}")
    logging.debug(f"Incoming intervals: {data.watched_intervals}")

    if data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    new_intervals = [i for i in data.watched_intervals if i[1] > i[0] and (i[1] - i[0]) >= 1.0]
    if not new_intervals:
        raise HTTPException(status_code=400, detail="No valid intervals to save")

    record = db.query(models.Progress).filter_by(
        user_id=data.user_id,
        video_id=data.video_id
    ).first()

    if record:
        logging.debug(f"Existing intervals: {record.watched_intervals}")
        combined = record.watched_intervals + new_intervals
        record.watched_intervals = merge_intervals(combined) 
        record.last_watched = max(record.last_watched or 0.0, data.last_watched or 0.0)
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

@app.get("/progress", response_model=schemas.ProgressOut)
def get_progress(
    video_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    try:
        record = crud.get_progress(db, current_user.id, video_id)
        if not record:
            raise HTTPException(status_code=404, detail="No progress found")
        return record
    except Exception as e:
        logging.error(f"Error fetching progress: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch progress")

@app.delete("/progress")
def delete_progress(
    video_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    record = crud.get_progress(db, current_user.id, video_id)
    if not record:
        raise HTTPException(status_code=404, detail="No progress found")
    logging.info(f"Deleting progress for user {current_user.id} on video {video_id}")
    db.delete(record)
    db.commit()
    return {"message": "Progress deleted successfully"}

# Root health check
@app.get("/")
def read_root():
    return {"message": "Hello from ProgressPal 🎬"}

@app.post("/reset_password")
def reset_password(user: schemas.UserResetPassword, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    new_password = auth.hash_password(user.new_password)
    crud.update_user_password(db, user.email, new_password)
    return {"message": "Password reset successfully"}

@app.get("/healthcheck")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}