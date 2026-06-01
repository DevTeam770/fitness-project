# 🏋️ Fitness Tracker

> אפליקציית כושר מלאה למעקב אחר אימונים, Progressive Overload ותיעוד התקדמות גופנית.
> **React Native (Expo)** בפרונט + **FastAPI** בבאקאנד.

---

## 📋 תוכן עניינים

- [סקירה כללית](#סקירה-כללית)
- [ארכיטקטורה וטכנולוגיות](#ארכיטקטורה-וטכנולוגיות)
- [מבנה הפרויקט](#מבנה-הפרויקט)
- [מודל הנתונים](#מודל-הנתונים)
- [API Endpoints](#api-endpoints)
- [הרצת הבאקאנד עם Docker](#הרצת-הבאקאנד-עם-docker)
- [הרצת הפרונט עם Expo](#הרצת-הפרונט-עם-expo)
- [משתני סביבה](#משתני-סביבה)
- [אבטחה](#אבטחה)

---

## סקירה כללית

Fitness Tracker מאפשר למשתמשים:

- 📝 **לתעד אימונים** – פתיחת אימון חי, הוספת סטים (משקל + חזרות) בזמן אמת וסגירת האימון
- 📈 **לעקוב אחר התקדמות** – גרף נפח אימון לאורך זמן ושיא אישי (PR) לפי תרגיל
- 🗂️ **לנהל תבניות אימון** – יצירת תוכניות (Push/Pull/Legs וכד') לשימוש חוזר
- 📸 **לתעד שינוי גופני** – העלאת תמונות התקדמות לאחסון בענן (MinIO/S3)

---

## ארכיטקטורה וטכנולוגיות

```
┌──────────────────────┐    ┌──────────────────┐    ┌──────────────┐
│  React Native (Expo) │───▶│  FastAPI Backend │───▶│  PostgreSQL  │
│  Android / iOS       │    │   (Port 8000)    │    │  (Port 5432) │
└──────────────────────┘    └──────────────────┘    └──────────────┘
                                      │
                                      ▼
                             ┌──────────────────┐
                             │  MinIO Storage   │
                             │  (Port 9000)     │
                             │  Console: 9001   │
                             └──────────────────┘
```

### Frontend

| שכבה | טכנולוגיה | תיאור |
|------|-----------|-------|
| Framework | **React Native 0.85** + **Expo 56** | אפליקציה נייטיב ל-Android ו-iOS |
| Language | **TypeScript 6** | טיפוסים סטטיים לכל הפרויקט |
| Navigation | **React Navigation 7** | ניווט Stack + Bottom Tabs |
| HTTP Client | **Axios** | קריאות API עם JWT interceptor אוטומטי |
| Storage | **AsyncStorage** | שמירת Token ופרטי משתמש מקומית |
| Charts | **Victory Native** | גרפי התקדמות ואנליטיקה |
| Icons | **Lucide React Native** | אייקונים לטאב-בר ולמסכים |

### Backend

| שכבה | טכנולוגיה | תיאור |
|------|-----------|-------|
| Web Framework | **FastAPI** 0.110+ | REST API עם תיעוד Swagger אוטומטי |
| ORM | **SQLAlchemy** 2.0 | גישה לבסיס הנתונים עם Typed Mapped Columns |
| Validation | **Pydantic** v2 | ולידציה ו-serialization של נתונים |
| Database | **PostgreSQL** 15 | בסיס נתונים ראשי |
| Object Storage | **MinIO** (S3-Compatible) | אחסון תמונות התקדמות |
| Auth | **JWT (python-jose)** | אימות משתמשים עם Access Token |
| Password Hashing | **Argon2** | הצפנת סיסמאות מאובטחת |
| Containerization | **Docker + Docker Compose** | הרצת כל שירותי הבאקאנד יחד |

---

## מבנה הפרויקט

```
fitness-project-main/
├── docker-compose.yml              # הגדרת שירותי הבאקאנד (DB, Storage, API)
├── .env                            # משתני סביבה (לא לשמור ב-Git!)
│
├── frontend/                       # אפליקציית React Native
│   ├── App.tsx                     # נקודת כניסה – NavigationContainer + AuthProvider
│   ├── index.ts
│   ├── app.json                    # הגדרות Expo (שם, אייקון, splash)
│   ├── package.json
│   ├── tsconfig.json
│   ├── assets/                     # אייקונים ותמונות אפליקציה
│   └── src/
│       ├── api/
│       │   └── client.ts           # Axios instance + JWT interceptor אוטומטי
│       ├── context/
│       │   └── AuthContext.tsx     # ניהול מצב התחברות (login/logout/token)
│       ├── navigation/
│       │   ├── AppNavigator.tsx    # Stack navigator – Login vs. Main
│       │   └── TabNavigator.tsx    # Bottom tabs (בית / אימון / גרפים / פרופיל)
│       ├── screens/
│       │   ├── LoginScreen.tsx     # מסך התחברות
│       │   ├── HomeScreen.tsx      # מסך הבית
│       │   ├── WorkoutScreen.tsx   # מסך אימון פעיל
│       │   ├── AnalyticsScreen.tsx # מסך גרפים ואנליטיקה
│       │   └── ProfileScreen.tsx   # מסך פרופיל ומעקב גופני
│       └── types/
│           └── index.ts            # TypeScript interfaces (User, Exercise, Session...)
│
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py                 # נקודת הכניסה, הגדרת FastAPI ו-CORS
        ├── database.py             # חיבור ל-PostgreSQL (SQLAlchemy engine)
        ├── models.py               # מודלי SQLAlchemy (טבלאות בבסיס הנתונים)
        ├── schemas.py              # מודלי Pydantic (request/response)
        ├── crud.py                 # פעולות CRUD על בסיס הנתונים
        ├── security.py             # יצירה ואימות של JWT tokens
        ├── dependencies.py         # Dependency Injection (get_current_user)
        ├── routers/
        │   ├── auth.py             # הרשמה והתחברות
        │   ├── users.py            # ניהול פרופיל משתמש
        │   ├── exercises.py        # ניהול מאגר תרגילים
        │   ├── sessions.py         # ניהול אימונים חיים
        │   ├── templates.py        # ניהול תבניות אימון
        │   ├── analytics.py        # נתוני התקדמות ו-PR
        │   └── history.py          # היסטוריית אימונים
        └── services/
            ├── storage.py          # שירות העלאה ל-MinIO/S3
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

## הרצת הבאקאנד עם Docker

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

## הרצת הפרונט עם Expo

### דרישות מקדימות

- Node.js מותקן
- Expo Go מותקן על הטלפון ([Android](https://play.google.com/store/apps/details?id=host.exp.exponent) / [iOS](https://apps.apple.com/app/expo-go/id982107779))
- הטלפון והמחשב על אותה רשת Wi-Fi

### שלבי התקנה

**1. עדכון כתובת ה-IP**

פתח את `frontend/src/api/client.ts` ועדכן את ה-IP למחשב שלך:
```typescript
const COMPUTER_IP = '192.168.X.X'; // ← שנה לכתובת ה-IP האמיתית שלך
```

> למציאת ה-IP: `ipconfig` (Windows) / `ifconfig` (Mac/Linux)

**2. התקנת תלויות**
```bash
cd frontend
npm install
```

**3. הפעלת שרת הפיתוח**
```bash
npm start
```

**4. סריקת QR Code**

סרוק את ה-QR Code שמופיע בטרמינל עם אפליקציית Expo Go על הטלפון.

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
- **Authentication** — מבוסס **JWT Bearer Token** עם תפוגה מוגדרת (30 ימים)
- **JWT Interceptor** — הפרונט מזריק את ה-Token אוטומטית לכל קריאת API דרך Axios interceptor
- **Persistent Session** — ה-Token נשמר ב-AsyncStorage ונטען בכל פתיחת אפליקציה
- **הגנה מ-IDOR** — כל endpoint בבאקאנד מוודא שהמשתמש המחובר הוא הבעלים של המשאב
- **ולידציה** — כל הקלטות עוברות ולידציה דרך Pydantic (מניעת ערכים לא תקינים)

---

## רישיון

פרויקט זה פרטי. כל הזכויות שמורות.
