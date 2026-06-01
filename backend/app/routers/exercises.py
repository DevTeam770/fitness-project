from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)

@router.get("/", response_model=list[schemas.ExerciseResponse])
def read_exercises(muscle: str | None = None, db: Session = Depends(get_db)):
    """
    שליפת כל התרגילים מהמאגר.
    ניתן להעביר Query Parameter בשם `muscle` כדי לסנן (למשל: /exercises?muscle=Chest)
    """
    exercises = crud.get_exercises(db, muscle=muscle)
    return exercises

@router.post("/", response_model=schemas.ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_new_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    """
    יצירת תרגיל חדש במאגר האפליקציה.
    מוודא שאין תרגיל אחר עם אותו שם כדי למנוע כפילויות.
    """
    # בדיקה אם התרגיל כבר קיים (לפי השם שלו)
    existing_exercises = crud.get_exercises(db)
    if any(ex.name.lower() == exercise.name.lower() for ex in existing_exercises):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise with this name already exists"
        )
    return crud.create_exercise(db, exercise=exercise)