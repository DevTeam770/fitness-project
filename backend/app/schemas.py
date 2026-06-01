from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


# ==========================================
# 1. SCHEMAS עבור משתמשים (User)
# ==========================================

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="סיסמה באורך 6 תווים לפחות")

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# 2. SCHEMAS עבור תרגילים (Exercise)
# ==========================================

class ExerciseBase(BaseModel):
    name: str
    target_muscle: str
    gif_url: str | None = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseResponse(ExerciseBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# 3. SCHEMAS עבור לוגים וסטים (WorkoutLog)
# ==========================================

class WorkoutLogBase(BaseModel):
    exercise_id: int
    set_number: int = Field(..., gt=0, description="מספר הסט חייב להיות גדול מ-0")
    weight: float = Field(..., ge=0, description="משקל לא יכול להיות שלילי")
    reps: int = Field(..., gt=0, description="מספר חזרות חייב להיות גדול מ-0")

class WorkoutLogCreate(WorkoutLogBase):
    pass

class WorkoutLogResponse(WorkoutLogBase):
    id: int
    session_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# ==========================================
# 4. SCHEMAS עבור אימונים בפועל (WorkoutSession)
# ==========================================

class WorkoutSessionBase(BaseModel):
    title: str
    template_id: int | None = None

class WorkoutSessionCreate(WorkoutSessionBase):
    pass

class WorkoutSessionUpdate(BaseModel):
    end_time: datetime | None = None
    is_completed: bool = False

# Schema מורחב שיוחזר לטלפון: כולל את כל הסטים שבוצעו בתוך האימון
class WorkoutSessionDetailedResponse(WorkoutSessionBase):
    id: int
    user_id: int
    start_time: datetime
    end_time: datetime | None
    is_completed: bool
    logs: list[WorkoutLogResponse] = []  # רשימת הסטים שבוצעו באימון זה

    class Config:
        from_attributes = True


# ==========================================
# 5. SCHEMAS עבור תבניות אימון (WorkoutTemplate)
# ==========================================

class WorkoutTemplateBase(BaseModel):
    title: str
    description: str | None = None

class WorkoutTemplateCreate(WorkoutTemplateBase):
    pass

class WorkoutTemplateResponse(WorkoutTemplateBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True




class VolumeHistoryPoint(BaseModel):
    date: date
    total_volume: float

    class Config:
        from_attributes = True

class ExerciseAnalyticsResponse(BaseModel):
    exercise_id: int
    exercise_name: str
    personal_record: float  # ה-PR המקסימלי
    volume_history: List[VolumeHistoryPoint]



class WorkoutTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    exercise_ids: List[int]  


class WorkoutTemplateResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    user_id: int
    exercises: List[ExerciseResponse]

    class Config:
        from_attributes = True


class ProgressPictureResponse(BaseModel):
    id: int
    image_url: str
    created_at: datetime

    class Config:
        from_attributes = True