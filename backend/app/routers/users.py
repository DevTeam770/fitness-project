from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db
from app.dependencies import get_current_user
from app.services.storage import storage_service
from app.services.notifications import notification_service

router = APIRouter(
    prefix="/users",
    tags=["User Management & Profile"]
)

@router.post("/progress-picture", response_model=schemas.ProgressPictureResponse, status_code=status.HTTP_201_CREATED)
def upload_progress_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """העלאת תמונת התקדמות (שינוי גופני) לענן המקומי ושמירת הקישור ב-DB"""
    # 1. העלאת הקובץ לשרת האחסון וקבלת ה-URL
    file_url = storage_service.upload_progress_picture(user_id=current_user.id, file=file)
    
    # 2. שמירת הרשומה בבסיס הנתונים
    db_picture = models.ProgressPicture(user_id=current_user.id, image_url=file_url)
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    
    # 3. פיצ'ר מסחרי: שליחת התראת Push למשתמש כטריגר עידוד על העלאת התמונה!
    notification_service.send_push_notification(
        user_id=current_user.id,
        title="כל הכבוד על ההתמדה! 💪",
        body="תמונת ההתקדמות שלך נשמרה בהצלחה. תמשיך ככה, התוצאות מגיעות!",
        data={"screen": "ProgressGallery"}
    )
    
    return db_picture