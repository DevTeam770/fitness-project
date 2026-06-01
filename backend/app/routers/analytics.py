from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics & Progress"]
)

@router.get("/exercise/{exercise_id}", response_model=schemas.ExerciseAnalyticsResponse)
def get_exercise_progress(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """קבלת נתוני התקדמות ומשקלי שיא עבור תרגיל ספציפי של המשתמש המחובר"""
    analytics = crud.get_exercise_analytics(db, exercise_id=exercise_id, user_id=current_user.id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return analytics