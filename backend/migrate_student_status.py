import sqlite3
from datetime import datetime

conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Dodaj status kolonu ako ne postoji
try:
    cursor.execute("ALTER TABLE students ADD COLUMN status VARCHAR DEFAULT 'PENDING'")
    print("Added status column")
except sqlite3.OperationalError as e:
    print(f"status: {e}")

# Dodaj created_at kolonu ako ne postoji
try:
    cursor.execute(f"ALTER TABLE students ADD COLUMN created_at DATETIME DEFAULT '{datetime.utcnow().isoformat()}'")
    print("Added created_at column")
except sqlite3.OperationalError as e:
    print(f"created_at: {e}")

conn.commit()
conn.close()

print("Database updated successfully!")
