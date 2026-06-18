"""
Pokreni iz backend/ foldera:
    python seed.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session
from app.database import engine
from app.models.user import User, UserRole
from app.models.mentor import Mentor
from app.models.mentorship_request import MentorshipRequest, RequestStatus  # POPRAVLJENO: ispravan import
from app.core.security import hash_password
from app.database import Base

# Kreiraj sve tablice
Base.metadata.create_all(bind=engine)

db = Session(engine)

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

# --- Test studentice ---
test_students = [
    {"email": "sara@test.com", "full_name": "Sara S.", "password_hash": hash_password("sara123"), "role": UserRole.member},
    {"email": "mia@test.com", "full_name": "Mia M.", "password_hash": hash_password("mia123"), "role": UserRole.member},
    {"email": "ana@test.com", "full_name": "Ana A.", "password_hash": hash_password("ana123"), "role": UserRole.member},
]

student_ids = {}
for s in test_students:
    existing = db.query(User).filter(User.email == s["email"]).first()
    if not existing:
        user = User(**s)
        db.add(user)
        db.commit()
        db.refresh(user)
        student_ids[s["email"]] = user.id
        print(f"✅ Studentica kreirana: {s['full_name']} ({s['email']})")
    else:
        student_ids[s["email"]] = existing.id
        print(f"ℹ️  Studentica već postoji: {s['email']}")

# --- Test mentorice (odobrene) ---
test_mentors = [
    {"first_name": "Lamija", "last_name": "Lara", "email": "lamija@mentor.com", "password": "lamija123", "field_of_expertise": "IT", "is_approved": True, "bio": "Iskusna IT stručnjakinja sa 5+ godina iskustva"},
    {"first_name": "Lejla", "last_name": "Lelić", "email": "lejla@mentor.com", "password": "lejla123", "field_of_expertise": "Biologija", "is_approved": True, "bio": "Biolog sa diplomom, volim da delim znanje"},
]

# --- Test mentorice na čekanju (za admin testove) ---
pending_mentors = [
    {"first_name": "Petra", "last_name": "Perić", "email": "petra@mentor.com", "field_of_expertise": "Hemija", "is_approved": False, "bio": "Hemičar sa iskustvom u istraživanju"},
    {"first_name": "Nina", "last_name": "Nović", "email": "nina@mentor.com", "field_of_expertise": "Fizika", "is_approved": False, "bio": "Fizičar i predavač na fakultetu"},
]

mentor_ids = {}

for m in test_mentors:
    email = m["email"]
    password = m.pop("password")

    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        user = User(
            email=email,
            full_name=f"{m['first_name']} {m['last_name']}",
            password_hash=hash_password(password),
            role=UserRole.mentor
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ User mentorica kreirana: {email}")

    existing = db.query(Mentor).filter(Mentor.email == email).first()
    if not existing:
        mentor = Mentor(**m)
        db.add(mentor)
        db.commit()
        db.refresh(mentor)
        mentor_ids[email] = mentor.id
        print(f"✅ Mentor profil kreiran: {m['first_name']} {m['last_name']}")
    else:
        mentor_ids[email] = existing.id
        print(f"ℹ️  Mentor već postoji: {email}")

for m in pending_mentors:
    email = m["email"]
    existing = db.query(Mentor).filter(Mentor.email == email).first()
    if not existing:
        mentor = Mentor(**m)
        db.add(mentor)
        db.commit()
        db.refresh(mentor)
        print(f"✅ Pending mentor kreiran: {m['first_name']} {m['last_name']}")
    else:
        print(f"ℹ️  Pending mentor već postoji: {email}")

# --- Test mentorship requests ---
if student_ids and mentor_ids:
    test_requests = [
        {
            "student_id": student_ids["sara@test.com"],       # POPRAVLJENO: student_id umjesto student_user_id
            "mentor_id": mentor_ids["lamija@mentor.com"],
            "message": "Zdravo, željela bih da radim sa vama na IT projektima!",
            "expectations": "Naučiti osnove programiranja",
            "skills_to_improve": "Python, Web development",
            "cv_file_path": "placeholder_cv.pdf",
            "status": RequestStatus.PENDING
        },
        {
            "student_id": student_ids["mia@test.com"],
            "mentor_id": mentor_ids["lamija@mentor.com"],
            "message": "Trebam help sa programiranjem, čula sam da ste odličan mentor",
            "expectations": "Unaprijediti vještine kodiranja",
            "skills_to_improve": "Algoritmi, Data structures",
            "cv_file_path": "placeholder_cv.pdf",
            "status": RequestStatus.PENDING
        },
        {
            "student_id": student_ids["ana@test.com"],
            "mentor_id": mentor_ids["lejla@mentor.com"],
            "message": "Zanimaju me biologijske nauke, možete li me mentorirati?",
            "expectations": "Razumjeti molekularnu biologiju",
            "skills_to_improve": "Istraživačke metode, Lab tehnika",
            "cv_file_path": "placeholder_cv.pdf",
            "status": RequestStatus.ACCEPTED
        },
    ]

    for req in test_requests:
        existing = db.query(MentorshipRequest).filter(
            MentorshipRequest.student_id == req["student_id"],
            MentorshipRequest.mentor_id == req["mentor_id"]
        ).first()
        if not existing:
            mr = MentorshipRequest(**req)
            db.add(mr)
            print(f"✅ Zahtjev kreiran: {req['status'].value} - student {req['student_id']} → mentor {req['mentor_id']}")
        else:
            print(f"ℹ️  Zahtjev već postoji")

    db.commit()

print("\n✅ Seed završen!")
print("\n📝 Test kredencijali:")
print("   Admin:             admin@test.com / admin123")
print("   Mentorica (Lamija): lamija@mentor.com / lamija123")
print("   Mentorica (Lejla):  lejla@mentor.com / lejla123")
print("   Studentica (Sara):  sara@test.com / sara123")
print("   Studentica (Mia):   mia@test.com / mia123")
print("   Studentica (Ana):   ana@test.com / ana123")

db.close()