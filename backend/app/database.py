import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# שליפת כתובת מסד הנתונים ישירות ממשתני הסביבה שהוזרקו דרך ה-Docker / .env
DATABASE_URL = os.getenv("DATABASE_URL")

# בדיקת בטיחות: אם משתנה הסביבה לא הוגדר, השרת יקרוס מיד בהפעלה עם שגיאה ברורה
# זה מונע מהאפליקציה לרוץ במצב "עיוור" בלי חיבור תקין ל-DB
if not DATABASE_URL:
    raise ValueError("ERROR: DATABASE_URL environment variable is not set!")

# יצירת המנוע (Engine) שמנהל את החיבורים הפיזיים ל-PostgreSQL
engine = create_engine(DATABASE_URL)

# יצירת מפעל לייצור Sessions (כרטיסי עבודה מול ה-DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# מחלקת הבסיס שממנה ירשו כל המודלים שלנו (SQLAlchemy Tables)
class Base(DeclarativeBase):
    pass

# Dependency (תלות) שנספק ל-FastAPI Routes כדי לקבל session נקי לכל בקשת HTTP
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()