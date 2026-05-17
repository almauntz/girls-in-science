from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.core.config import settings
from app.database import create_db
from app.routers import auth, mentoring, workshops, profiles, role_models, news
from app.core.security import get_current_user
from app.models.user import User
from app.models.role_model import RoleModel

create_db()

security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    description="Platform backend for Girls in Science centre",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
