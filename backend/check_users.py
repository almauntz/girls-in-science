import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()

users = db.query(User).all()
print(f"\n📋 Korisnici u bazi ({len(users)} total):\n")
for u in users:
    print(f"  • {u.email} (ID: {u.id}, Role: {u.role.value})")
    print(f"    Full name: {u.full_name}")
    print(f"    Password hash exists: {bool(u.password_hash)}")
    print()
