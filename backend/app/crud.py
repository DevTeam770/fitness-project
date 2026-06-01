from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app import models, schemas
from app.security import hash_password
from app.models import Exercise, WorkoutSession, WorkoutLog, WorkoutTemplate

# ==========================================
# 1. PURE USER OPERATIONS
# ==========================================

def get_user_by_email(db: Session, email: str):
    """שליפת משתמש לפי אימייל (עבור תהליך ההתחברות)"""
    return db.execute(select(models.User).where(models.User.email == email)).scalar_one_or_none()

def create_user(db: Session, user: schemas.UserCreate):
    """יצירת משתמש חדש והצפנת הסיסמה שלו עם Argon2"""
    hashed_pwd = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ==========================================
# 2. EXERCISE OPERATIONS
# ==========================================

def get_exercises(db: Session, muscle: str | None = None):
    """שליפת כל התרגילים, עם אפשרות לסינון לפי קבוצת שריר"""
    query = select(models.Exercise)
    if muscle:
        query = query.where(models.Exercise.target_muscle == muscle)
    return db.execute(query).scalars().all()

def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    """הוספת תרגיל חדש למאגר האפליקציה"""
    db_exercise = models.Exercise(**exercise.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


# ==========================================
# 3. WORKOUT SESSION & LOGGING OPERATIONS
# ==========================================

def create_workout_session(db: Session, session_data: schemas.WorkoutSessionCreate, user_id: int):
    """יצירת מופע של אימון חדש (כשלוחצים 'התחל אימון' בטלפון)"""
    db_session = models.WorkoutSession(
        title=session_data.title,
        template_id=session_data.template_id,
        user_id=user_id,
        start_time=datetime.utcnow(),
        is_completed=False
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def add_workout_log(db: Session, log_data: schemas.WorkoutLogCreate, session_id: int):
    """שמירת סט בודד שבוצע בפועל (בזמן לחיצה על וי באימון)"""
    db_log = models.WorkoutLog(
        session_id=session_id,
        exercise_id=log_data.exercise_id,
        set_number=log_data.set_number,
        weight=log_data.weight,
        reps=log_data.reps,
        timestamp=datetime.utcnow()
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_workout_session_detailed(db: Session, session_id: int, user_id: int):
    """שליפת אימון ספציפי כולל כל הסטים שבוצעו בתוכו (Eager Loading)"""
    return db.execute(
        select(models.WorkoutSession)
        .where(models.WorkoutSession.id == session_id, models.WorkoutSession.user_id == user_id)
    ).scalar_one_or_none()

def complete_workout_session(db: Session, session_id: int, user_id: int):
    """סגירת אימון ועדכון שעת סיום (כשלוחצים 'סיים אימון')"""
    db_session = db.execute(
        select(models.WorkoutSession).where(
            models.WorkoutSession.id == session_id, 
            models.WorkoutSession.user_id == user_id
        )
    ).scalar_one_or_none()
    
    if db_session:
        db_session.is_completed = True
        db_session.end_time = datetime.utcnow()
        db.commit()
        db.refresh(db_session)
    return db_session



def get_exercise_analytics(db: Session, exercise_id: int, user_id: int):
    """
    מחשב את משקל השיא (PR) ואת היסטוריית נפח העבודה לאורך זמן עבור תרגיל ספציפי של משתמש.
    """
    # 1. שליפת שם התרגיל
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None

    # 2. חישוב ה-PR (המשקל המקסימלי שהמשתמש הרים בתרגיל זה)
    # אנחנו מחברים את ה-Logs ל-Sessions כדי לוודא שזה שייך למשתמש הנוכחי
    pr_query = db.query(func.max(WorkoutLog.weight)).\
        join(WorkoutSession, WorkoutSession.id == WorkoutLog.session_id).\
        filter(WorkoutLog.exercise_id == exercise_id, WorkoutSession.user_id == user_id).scalar()
    
    personal_record = pr_query if pr_query else 0.0

    # 3. חישוב נפח עבודה כולל (Weight * Reps) לפי תאריך (ליצירת גרף)
    # מקבצים (Group By) לפי תאריך האימון ומסכמים את הנפח של כל הסטים באותו יום
    volume_query = db.query(
        func.date(WorkoutSession.start_time).label("workout_date"),
        func.sum(WorkoutLog.weight * WorkoutLog.reps).label("daily_volume")
    ).\
        join(WorkoutLog, WorkoutLog.session_id == WorkoutSession.id).\
        filter(WorkoutLog.exercise_id == exercise_id, WorkoutSession.user_id == user_id).\
        group_by(func.date(WorkoutSession.start_time)).\
        order_by(func.date(WorkoutSession.start_time)).all()

    # עיצוב התוצאה למבנה ה-Schema
    volume_history = [
        {"date": row.workout_date, "total_volume": row.daily_volume}
        for row in volume_query
    ]

    return {
        "exercise_id": exercise_id,
        "exercise_name": exercise.name,
        "personal_record": personal_record,
        "volume_history": volume_history
    }

def create_workout_template(db: Session, template_data: WorkoutTemplate, user_id: int):
    """יצירת תבנית אימון חדשה וקישור התרגילים הרלוונטיים אליה"""
    # 1. יצירת אובייקט התבנית הבסיסי
    db_template = WorkoutTemplate(
        name=template_data.name,
        description=template_data.description,
        user_id=user_id
    )
    
    # 2. שליפת התרגילים מה-DB לפי ה-IDs שהתקבלו וחיבורם לתבנית (SQLAlchemy מנהל את טבלת הקשר אוטומטית)
    if template_data.exercise_ids:
        exercises = db.query(Exercise).filter(Exercise.id.in_(template_data.exercise_ids)).all()
        db_template.exercises = exercises

    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def get_user_templates(db: Session, user_id: int):
    """שליפת כל תבניות האימון השייכות למשתמש מסוים"""
    return db.query(WorkoutTemplate).filter(WorkoutTemplate.user_id == user_id).all()