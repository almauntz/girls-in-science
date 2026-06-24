from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.database import create_db
from app.core.security import get_current_user
from app.models.user import User

from app.routers import (
    auth, mentoring, workshops, profiles,
    role_models, news, admin, requests, students
)
from app.routers import admin_users
from app.routers import bookmarks


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    description="Platform backend for Girls in Science centre",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(workshops.router)
app.include_router(mentoring.router)
app.include_router(role_models.router)
app.include_router(news.router)
app.include_router(profiles.router)
app.include_router(students.router)
app.include_router(admin.router)
app.include_router(admin_users.router)
app.include_router(requests.router)
app.include_router(bookmarks.router)


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


# Prilagođena klasa koja forsira browser da otvori PDF inline umjesto downloada
class PDFStaticFiles(StaticFiles):
    def file_response(self, pool_line, stat_result, scope, status_code=200):
        response = super().file_response(pool_line, stat_result, scope, status_code)
        if isinstance(response, FileResponse) and response.path.endswith('.pdf'):
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = "inline"
        return response


# OSIGURAVANJE DA FOLDERI POSTOJE
os.makedirs("static", exist_ok=True)
os.makedirs("uploads/cv", exist_ok=True)
os.makedirs("uploads/student_cvs", exist_ok=True)


# =========================================================================
# NOVA ZAMJENSKA RUTA: Preusmjerava studentske CV-jeve na folder od mentora
# =========================================================================
@app.get("/uploads/student_cvs/{filename}")
async def get_student_cv_from_mentor_folder(filename: str):
    # Tražimo fajl unutar 'uploads/cv' (gdje su mentori) umjesto 'student_cvs'
    target_path = os.path.join("uploads", "cv", filename)
    
    # Ako taj konkretan fajl ne postoji, uzimamo PRVI slobodan PDF iz uploads/cv (npr. Belmin CV)
    if not os.path.exists(target_path):
        mentor_files = [f for f in os.listdir("uploads/cv") if f.endswith('.pdf')]
        if mentor_files:
            target_path = os.path.join("uploads", "cv", mentor_files[0])
        else:
            raise HTTPException(status_code=404, detail="Nijedan CV nije pronađen u uploads/cv")

    # Vraćamo fajl tako da se otvori inline u browseru (isto kao kod mentorice)
    return FileResponse(
        target_path, 
        media_type="application/pdf", 
        headers={"Content-Disposition": "inline"}
    )
# =========================================================================


app.mount("/static", PDFStaticFiles(directory="static"), name="static")
app.mount("/uploads", PDFStaticFiles(directory="uploads"), name="uploads")