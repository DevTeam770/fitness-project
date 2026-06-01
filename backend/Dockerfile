# משתמשים באימג' רשמי וקל משקל של פייתון 3.11
FROM python:3.11-slim

# הגדרת תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# מניעת פייתון מלכתוב קבצי pyc לדיסק ומניעת buffering של ה-output (טוב ללוגים בזמן אמת)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# העתקת קובץ הדרישות והתקנת החבילות
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# העתקת שאר קוד המקור של האפליקציה (התיקייה app)
COPY . /app

# חשיפת הפורט שבו השרת רץ
EXPOSE 8000