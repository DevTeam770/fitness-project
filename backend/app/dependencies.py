import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import crud, models
from app.database import get_db

# מגדיר ל-FastAPI מאיפה לקחת את ה-Token (במקרה של OAuth2, שדה Authorization ב-Header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """
    חוסם גישה לראוטר, מאמת את ה-JWT, ומחזיר את המשתמש המחובר הנוכחי.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # פענוח ה-Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # שליפת המשתמש מתוך ה-DB לפי האימייל שחולץ מה-Token
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user