from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user 

router = APIRouter(
    prefix="/sessions",
    tags=["Workout Sessions"]
)

@router.post("/", response_model=schemas.WorkoutSessionDetailedResponse, status_code=status.HTTP_201_CREATED)
def start_new_workout(
    session_data: schemas.WorkoutSessionCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """יצירת מופע של אימון חדש עבור המשתמש המחובר הנוכחי"""
    return crud.create_workout_session(db, session_data=session_data, user_id=current_user.id)


@router.post("/{session_id}/logs", response_model=schemas.WorkoutLogResponse, status_code=status.HTTP_201_CREATED)
def log_set(
    session_id: int, 
    log_data: schemas.WorkoutLogCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """שמירת סט בודד (משקל וחזרות) בתוך האימון הנוכחי של המשתמש"""
    # בדיקה שהאימון קיים ושייך ספציפית למשתמש המחובר (מונע פירצת IDOR)
    session = crud.get_workout_session_detailed(db, session_id=session_id, user_id=current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Workout session not found")
    
    if session.is_completed:
        raise HTTPException(status_code=400, detail="Cannot add sets to a completed workout session")

    return crud.add_workout_log(db, log_data=log_data, session_id=session_id)


@router.get("/{session_id}", response_model=schemas.WorkoutSessionDetailedResponse)
def get_workout_details(
    session_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """שליפת אימון מסוים כולל הסטים שלו – רק אם האימון שייך למשתמש המחובר"""
    session = crud.get_workout_session_detailed(db, session_id=session_id, user_id=current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Workout session not found")
    return session


@router.post("/{session_id}/complete", response_model=schemas.WorkoutSessionDetailedResponse)
def finish_workout(
    session_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) 
):
    """סגירת אימון ועדכון שעת סיום עבור המשתמש הנוכחי"""
    session = crud.complete_workout_session(db, session_id=session_id, user_id=current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Workout session not found")
    return session