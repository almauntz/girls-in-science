import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, hash_password

db = SessionLocal()

admin = db.query(User).filter(User.email == "admin@test.com").first()

if admin:
    print(f"\n🔍 Admin korisnik pronađen:")
    print(f"   Email: {admin.email}")
    print(f"   Password hash: {admin.password_hash[:50]}...")
    
    test_password = "admin123"
    is_valid = verify_password(test_password, admin.password_hash)
    print(f"\n   ✓ Testiranje 'admin123': {is_valid}")
    
    # Kreiram novi hash da vidim kako izgleda
    new_hash = hash_password("admin123")
    print(f"\n   Novi hash: {new_hash}")
    print(f"   Verifikacija novog: {verify_password('admin123', new_hash)}")
else:
    print("Admin nije pronađen!")
