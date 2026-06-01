import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# אתחול המצפין של Argon2
ph = PasswordHasher()

# משיכת משתני הסביבה (שהגדרנו ב-.env)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

def hash_password(password: str) -> str:
    """הופך סיסמה נקייה ל-Hash מוצפן ומאובטח באמצעות Argon2"""
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """בודק האם הסיסמה שהוקלדה מתאימה ל-Hash השמור ב-DB"""
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

def create_access_token(data: dict) -> str:
    """מייצר אסימון JWT מוצפן החתום על ידי השרת שלנו"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt