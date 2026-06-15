from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import DeclarativeBase, registry
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Single metadata registry — all models (SQLModel + plain SQLAlchemy) share this.
# DeclarativeBase subclass pointing at SQLModel.metadata ensures foreign key
# references between SQLModel tables (users) and SQLAlchemy tables (mentors,
# students, mentorship_requests) resolve correctly at mapper configuration time.
class Base(DeclarativeBase):
    metadata = SQLModel.metadata  # type: ignore[assignment]

def create_db():
    # Import ALL models so every table is registered before create_all runs
    from app.models.user import User                          # noqa: F401
    from app.models.mentor import Mentor                      # noqa: F401
    from app.models.student import Student                    # noqa: F401
    from app.models.mentorship_request import MentorshipRequest  # noqa: F401
    from app.models.role_model import RoleModel               # noqa: F401
    from app.models.news import NewsPost, NewsCategory, NewsCategoryLink, NewsPostRoleModelLink  # noqa: F401
    from app.models.profile import Profile, WorkshopRegistration, Workshop as ProfileWorkshop  # noqa: F401
    from app.models.workshops_models import Workshop, WorkshopProposal, Registration, WorkshopRating, UserNotification, WaitingList  # noqa: F401
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
