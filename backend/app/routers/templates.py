from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/templates",
    tags=["Workout Templates"]
)

@router.post("/", response_model=schemas.WorkoutTemplateResponse, status_code=status.HTTP_201_CREATED)
def create_template(
    template_data: schemas.WorkoutTemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """יצירת תבנית אימון אישית עבור המשתמש המחובר"""
    return crud.create_workout_template(db, template_data=template_data, user_id=current_user.id)


@router.get("/", response_model=List[schemas.WorkoutTemplateResponse])
def list_my_templates(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """שליפת כל תבניות האימון של המשתמש המחובר"""
    return crud.get_user_templates(db, user_id=current_user.id)