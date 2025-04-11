from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base
from . import crud, schemas
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Lecture Video Progress Tracker")

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to ["http://localhost:3000"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/progress", response_model=schemas.ProgressOut)
def save_progress(progress: schemas.ProgressCreate, db: Session = Depends(get_db)):
    try:
        return crud.save_progress(db, progress)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Welcome to the Lecture Video Progress Tracker API!"}

@app.get("/progress", response_model=schemas.ProgressOut)
def get_progress(user_id: str, video_id: str, db: Session = Depends(get_db)):
    record = crud.get_progress(db, user_id, video_id)
    if not record:
        raise HTTPException(status_code=404, detail="No progress found")
    return record
