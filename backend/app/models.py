from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # קשרים (Relationships)
    templates: Mapped[list["WorkoutTemplate"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[list["WorkoutSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    progress_pictures: Mapped[list["ProgressPicture"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    target_muscle: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # חזה, גב, רגליים וכו'
    gif_url: Mapped[str | None] = mapped_column(String(255), nullable=True)  # להצגת סרטון הדגמה קצר באפליקציה

    # קשר ללוגים שבוצעו בפועל
    logs: Mapped[list["WorkoutLog"]] = relationship(back_populates="exercise")


class WorkoutTemplate(Base):
    """
    תבנית של אימון מובנה מראש (למשל: אימון Push, אימון Pull)
    """
    __tablename__ = "workout_templates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)  # שם התוכנית
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # קשרים
    user: Mapped["User"] = relationship(back_populates="templates")
    sessions: Mapped[list["WorkoutSession"]] = relationship(back_populates="template")


class WorkoutSession(Base):
    """
    אימון ספציפי שמתבצע בזמן אמת בחדר הכושר
    """
    __tablename__ = "workout_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    template_id: Mapped[int | None] = mapped_column(ForeignKey("workout_templates.id"), nullable=True)
    
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # מתי לחצת "סיים אימון"
    is_completed: Mapped[bool] = mapped_column(default=False)  # סטטוס האימון

    # קשרים
    user: Mapped["User"] = relationship(back_populates="sessions")
    template: Mapped["WorkoutTemplate"] = relationship(back_populates="sessions")
    logs: Mapped[list["WorkoutLog"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class WorkoutLog(Base):
    """
    שורת לוג בודדת המייצגת סט אחד של תרגיל שבוצע בפועל
    """
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("workout_sessions.id"), nullable=False)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False)
    
    set_number: Mapped[int] = mapped_column(Integer, nullable=False)  # סט 1, סט 2...
    weight: Mapped[float] = mapped_column(Float, nullable=False)       # משקל בק"ג
    reps: Mapped[int] = mapped_column(Integer, nullable=False)        # חזרות שבוצעו
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow) # זמן ביצוע הסט

    # קשרים
    session: Mapped["WorkoutSession"] = relationship(back_populates="logs")
    exercise: Mapped["Exercise"] = relationship(back_populates="logs")


class ProgressPicture(Base):
    """
    טבלת מעקב שינוי גופני - תמונות התקדמות המקושרות לענן האחסון
    """
    __tablename__ = "progress_pictures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)  # הקישור שנוצר ב-MinIO/S3
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # קשרים
    user: Mapped["User"] = relationship(back_populates="progress_pictures")