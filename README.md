# 🏋️ Fitness Tracker API

> Backend API לניהול אימוני כושר, מעקב אחר Progressive Overload ותיעוד התקדמות גופנית.

---

## 📋 תוכן עניינים

- [סקירה כללית](#סקירה-כללית)
- [ארכיטקטורה וטכנולוגיות](#ארכיטקטורה-וטכנולוגיות)
- [מבנה הפרויקט](#מבנה-הפרויקט)
- [מודל הנתונים](#מודל-הנתונים)
- [API Endpoints](#api-endpoints)
- [הרצה מקומית עם Docker](#הרצה-מקומית-עם-docker)
- [משתני סביבה](#משתני-סביבה)
- [אבטחה](#אבטחה)

---

## סקירה כללית

Fitness Tracker API הוא שרת Backend שנבנה עם **FastAPI** ומאפשר למשתמשים:

- 📝 **לתעד אימונים** – פתיחת אימון חי, הוספת סטים (משקל + חזרות) בזמן אמת וסגירת האימון
- 📈 **לעקוב אחר התקדמות** – צפייה בגרף נפח אימון לאורך זמן ורשומות שיא אישי (PR) לפי תרגיל
- 🗂️ **לנהל תבניות אימון** – יצירת תוכניות (Push/Pull/Legs וכד') לשימוש חוזר
- 📸 **לתעד שינוי גופני** – העלאת תמונות התקדמות לאחסון בענן (MinIO/S3)

---

## ארכיטקטורה וטכנולוגיות

```
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐
│   Client    │───▶│  FastAPI Backend │───▶│  PostgreSQL  │
│  (Mobile)   │    │   (Port 8000)    │    │  (Port 5432) │
└─────────────┘    └──────────────────┘    └──────────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │  MinIO Storage   │
                   │  (Port 9000)     │
                   │  Console: 9001   │
                   └──────────────────┘
```

| שכבה | טכנולוגיה | תיאור |
|------|-----------|-------|
| Web Framework | **FastAPI** 0.110+ | בניית REST API עם תיעוד Swagger אוטומטי |
| ORM | **SQLAlchemy** 2.0 | גישה לבסיס הנתונים עם Typed Mapped Columns |
| Validation | **Pydantic** v2 | ולידציה ו-serialization של נתונים |
| Database | **PostgreSQL** 15 | בסיס נתונים ראשי |
| Object Storage | **MinIO** (S3-Compatible) | אחסון תמונות התקדמות |
| Auth | **JWT (python-jose)** | אימות משתמשים עם Access Token |
| Password Hashing | **Argon2** | הצפנת סיסמאות מאובטחת |
| Containerization | **Docker + Docker Compose** | הרצת כל השירותים יחד |
| ASGI Server | **Uvicorn** | הרצת FastAPI בפרודקשן |

---

## מבנה הפרויקט

```
fitness-project-main/
├── docker-compose.yml          # הגדרת כל השירותים (DB, Storage, Backend)
├── .env                        # משתני סביבה (לא לשמור ב-Git!)
│
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py             # נקודת הכניסה, הגדרת FastAPI ו-CORS
        ├── database.py         # חיבור ל-PostgreSQL (SQLAlchemy engine)
        ├── models.py           # מודלי SQLAlchemy (טבלאות בבסיס הנתונים)
        ├── schemas.py          # מודלי Pydantic (request/response)
        ├── crud.py             # פעולות CRUD על בסיס הנתונים
        ├── security.py         # יצירה ואימות של JWT tokens
        ├── dependencies.py     # Dependency Injection (get_current_user)
        │
        ├── routers/
        │   ├── auth.py         # הרשמה והתחברות
        │   ├── users.py        # ניהול פרופיל משתמש
        │   ├── exercises.py    # ניהול מאגר תרגילים
        │   ├── sessions.py     # ניהול אימונים חיים
        │   ├── templates.py    # ניהול תבניות אימון
        │   ├── analytics.py    # נתוני התקדמות ו-PR
        │   └── history.py      # היסטוריית אימונים
        │
        └── services/
            ├── storage.py      # שירות העלאה ל-MinIO/S3
            └── notifications.py
```

---

## מודל הנתונים

```
User (משתמש)
 ├── WorkoutTemplate (תבנית אימון)
 │    └── WorkoutSession (אימון ספציפי)
 │         └── WorkoutLog (סט בודד: תרגיל + משקל + חזרות)
 ├── WorkoutSession
 │    └── WorkoutLog
 │         └── Exercise (תרגיל: שם + שריר + GIF)
 └── ProgressPicture (תמונת התקדמות)
```

### טבלאות מרכזיות

| טבלה | תיאור | שדות מרכזיים |
|------|-------|-------------|
| `users` | משתמשי המערכת | `email`, `hashed_password`, `full_name` |
| `exercises` | מאגר תרגילים גלובלי | `name`, `target_muscle`, `gif_url` |
| `workout_templates` | תבניות אימון של משתמש | `title`, `description`, `user_id` |
| `workout_sessions` | מופע אימון בפועל | `start_time`, `end_time`, `is_completed` |
| `workout_logs` | סט בודד שבוצע | `exercise_id`, `set_number`, `weight`, `reps` |
| `progress_pictures` | תמונות התקדמות | `image_url`, `user_id`, `created_at` |

---

## API Endpoints

### 🔐 Authentication — `/auth`

| Method | Endpoint | תיאור |
|--------|----------|-------|
| `POST` | `/auth/register` | הרשמת משתמש חדש |
| `POST` | `/auth/login` | התחברות וקבלת JWT Token |

### 💪 Exercises — `/exercises`

| Method | Endpoint | תיאור |
|--------|----------|-------|
| `GET` | `/exercises` | רשימת כל התרגילים |
| `POST` | `/exercises` | הוספת תרגיל חדש למאגר |

### 🏃 Workout Sessions — `/sessions`

| Method | Endpoint | תיאור |
|--------|----------|-------|
| `POST` | `/sessions` | פתיחת אימון חדש |
| `GET` | `/sessions/{id}` | שליפת פרטי אימון כולל סטים |
| `POST` | `/sessions/{id}/logs` | הוספת סט (משקל + חזרות) לאימון |
| `POST` | `/sessions/{id}/complete` | סיום וסגירת האימון |

### 📊 Analytics — `/analytics`

| Method | Endpoint | תיאור |
|--------|----------|-------|
| `GET` | `/analytics/exercise/{id}` | גרף נפח + שיא אישי לתרגיל |

### 📋 Templates — `/templates`

| Method | Endpoint | תיאור |
|--------|----------|-------|
| `POST` | `/templates` | יצירת תבנית אימון |
| `GET` | `/templates` | רשימת התבניות של המשתמש |

> **📖 תיעוד API אינטראקטיבי:** לאחר הרצה, זמין בכתובת `http://localhost:8000/docs`

---

## הרצה מקומית עם Docker

### דרישות מקדימות

- [Docker](https://www.docker.com/) ו-Docker Compose מותקנים

### שלבי התקנה

**1. שכפול הפרויקט**
```bash
git clone <REPO_URL>
cd fitness-project-main
```

**2. הגדרת משתני סביבה**
```bash
cp .env.example .env
# ערוך את .env עם הערכים שלך
```

**3. הפעלת כל השירותים**
```bash
docker compose up --build
```

**4. בדיקה שהכל עובד**
```bash
curl http://localhost:8000/
# { "status": "healthy", "message": "Fitness Tracker API is up and running!" }
```

### שירותים פעילים לאחר ההרצה

| שירות | כתובת | תיאור |
|-------|-------|-------|
| FastAPI | `http://localhost:8000` | ה-API הראשי |
| Swagger UI | `http://localhost:8000/docs` | תיעוד API אינטראקטיבי |
| PostgreSQL | `localhost:5432` | בסיס הנתונים |
| MinIO Console | `http://localhost:9001` | ממשק ניהול אחסון |

---

## משתני סביבה

קובץ `.env` בשורש הפרויקט:

```env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
POSTGRES_DB=fitness_tracker
DB_HOST=db
DB_PORT=5432

# JWT Security
SECRET_KEY=your_secret_key_here        # שנה לסוד חזק בפרודקשן!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200      # 30 ימים
```

> ⚠️ **חשוב:** לעולם אל תשמור את קובץ `.env` עם סיסמאות אמיתיות ב-Git. הוסף אותו ל-`.gitignore`.

---

## אבטחה

- **סיסמאות** — מוצפנות עם **Argon2** (אלגוריתם ה-hashing המומלץ ביותר כיום)
- **Authentication** — מבוסס **JWT Bearer Token** עם תפוגה מוגדרת
- **הגנה מ-IDOR** — כל endpoint מוודא שהמשהשתמש המחובר הוא הבעלים של המשאב
- **ולידציה** — כל הקלטות עוברות ולידציה דרך Pydantic (מניעת ערכים לא תקינים)

---

## רישיון

פרויקט זה פרטי. כל הזכויות שמורות.
