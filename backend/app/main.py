from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import exercises, sessions, auth, analytics, templates, users

# יצירת הטבלאות ב-PostgreSQL אוטומטית
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness Tracker API",
    description="Backend API for managing workouts and tracking progressive overload",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)  
app.include_router(exercises.router)
app.include_router(sessions.router)
app.include_router(analytics.router)
app.include_router(templates.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Fitness Tracker API is up and running!"}