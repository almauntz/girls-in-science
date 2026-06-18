from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text, inspect
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

def run_migrations():
    """Automatski dodaje kolone koje nedostaju u postojećim tabelama."""
    inspector = inspect(engine)

    with engine.connect() as conn:
        # --- profiles tabela ---
        if "profiles" in inspector.get_table_names():
            existing = [col["name"] for col in inspector.get_columns("profiles")]
            new_columns = {
                "languages": "VARCHAR",
                "experience": "VARCHAR",
                "education": "VARCHAR",
                "skills": "VARCHAR",
                "linkedin_url": "VARCHAR",
                "github_url": "VARCHAR",
                "twitter_url": "VARCHAR",
            }
            for col_name, col_type in new_columns.items():
                if col_name not in existing:
                    conn.execute(text(f"ALTER TABLE profiles ADD COLUMN {col_name} {col_type}"))
                    print(f"[migration] Dodana kolona: profiles.{col_name}")

        conn.commit()

def create_db():
    # Import ALL models so every table is registered before create_all runs
    from app.models.user import User                          # noqa: F401
    from app.models.mentor import Mentor                      # noqa: F401
    from app.models.student import Student                    # noqa: F401
    from app.models.mentorship_request import MentorshipRequest  # noqa: F401
    from app.models.role_model import RoleModel               # noqa: F401
    from app.models.news import NewsPost, NewsCategory, NewsCategoryLink, NewsPostRoleModelLink  # noqa: F401
    from app.models.profile import Profile                    # noqa: F401
    from app.models.workshops_models import Workshop, WorkshopProposal, Registration, WorkshopRating, UserNotification, WaitingList  # noqa: F401
    SQLModel.metadata.create_all(engine)
    run_migrations()  # dodaje kolone koje nedostaju u postojećim bazama

def get_db():
    with Session(engine) as session:
        yield session
