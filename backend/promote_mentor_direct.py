"""
Direktno prebacivanje user-a iz member u mentor status
Pokreni iz backend/ foldera:
    python promote_mentor_direct.py
"""
import sqlite3
import os
from datetime import datetime

# Pronađi bazu
db_path = "sql_app.db"

if not os.path.exists(db_path):
    print(f"❌ Baza podataka nije pronađena na: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

email = "lamija@mentor.com"

print(f"🔍 Tražim user sa emailom: {email}")

# 1. Pronađi user i njegov id
cursor.execute("SELECT id, email, full_name, role FROM users WHERE email = ?", (email,))
user = cursor.fetchone()

if not user:
    print(f"❌ User sa email-om '{email}' nije pronađen!")
    conn.close()
    exit(1)

user_id, user_email, user_name, current_role = user
print(f"✅ Pronađen user:")
print(f"   ID: {user_id}")
print(f"   Email: {user_email}")
print(f"   Ime: {user_name}")
print(f"   Trenutna rola: {current_role}")

# 2. Pronađi da li postoji već mentor profil
cursor.execute("SELECT id, email FROM mentors WHERE email = ?", (email,))
mentor = cursor.fetchone()

if mentor:
    print(f"\n✅ Mentor profil već postoji (ID: {mentor[0]})")
    mentor_id = mentor[0]
else:
    print(f"\n📝 Kreiram novi Mentor profil...")
    # Rasclani ime
    name_parts = user_name.split() if user_name else ["First", "Last"]
    first_name = name_parts[0] if len(name_parts) > 0 else "First"
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else "Last"
    
    cursor.execute("""
        INSERT INTO mentors 
        (first_name, last_name, email, field_of_expertise, is_approved, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, email, "Not specified yet", True, "APPROVED"))
    
    conn.commit()
    mentor_id = cursor.lastrowid
    print(f"✅ Mentor profil kreiran (ID: {mentor_id})")

# 3. Promijeni role u users tabeli na 'mentor'
if current_role != "mentor":
    cursor.execute("UPDATE users SET role = ? WHERE email = ?", ("mentor", email))
    conn.commit()
    print(f"\n🔄 Rola promijenjena: {current_role} → mentor")
else:
    print(f"\n✅ Rola je već 'mentor'")

conn.close()

print(f"\n" + "="*60)
print(f"✨ USPJEŠNO!")
print(f"="*60)
print(f"User:       {user_name}")
print(f"Email:      {email}")
print(f"Novi role:  mentor")
print(f"Mentor ID:  {mentor_id}")
print(f"Status:     APPROVED")
