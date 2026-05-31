from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.core.config import settings
from app.database import Base, engine
from app.routers import auth, mentoring, forum, workshops, profiles, students
from app.core.security import get_current_user
from app.models.user import User
from app.models.mentor import Mentor
from app.routers import admin  # u import sekciji
from app.models.student import Student
from app.routers import requests
from app.models.mentorship_request import MentorshipRequest

Base.metadata.create_all(bind=engine)

security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    description="Platform backend for Girls in Science centre",
    version="1.0.0"
)

# CORS middleware MORA biti dodan PRE ruta
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sada dodaj rute POSLE middleware-a
app.include_router(auth.router)
app.include_router(workshops.router)
app.include_router(mentoring.router)
app.include_router(forum.router)
app.include_router(profiles.router)
app.include_router(students.router)
app.include_router(admin.router)  # ispod ostalih routera
app.include_router(requests.router)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} API is running"}

@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role
    }

