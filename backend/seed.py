"""
Pokreni iz backend/ foldera:
    python seed.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.mentor import Mentor
from app.core.security import hash_password
from app.database import Base

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Admin korisnik ---
existing_admin = db.query(User).filter(User.email == "admin@test.com").first()
if not existing_admin:
    admin = User(
        email="admin@test.com",
        full_name="Admin User",
        password_hash=hash_password("admin123"),
        role=UserRole.admin
    )
    db.add(admin)
    db.commit()
    print("✅ Admin korisnik kreiran: admin@test.com / admin123")
else:
    print("ℹ️  Admin već postoji")

# --- Test mentorice (is_approved = False) ---
test_mentors = [
    {"first_name": "Ana", "last_name": "Anić", "email": "ana@test.com", "field_of_expertise": "IT"},
    {"first_name": "Mia", "last_name": "Mić", "email": "mia@test.com", "field_of_expertise": "Biologija"},
    {"first_name": "Lejla", "last_name": "Lejlić", "email": "lejla@test.com", "field_of_expertise": "Hemija"},
]

for m in test_mentors:
    existing = db.query(Mentor).filter(Mentor.email == m["email"]).first()
    if not existing:
        mentor = Mentor(**m, is_approved=False)
        db.add(mentor)
        print(f"✅ Mentorica kreirana: {m['first_name']} {m['last_name']}")
    else:
        print(f"ℹ️  Mentorica već postoji: {m['email']}")

db.commit()
db.close()
print("\n✅ Seed završen!")